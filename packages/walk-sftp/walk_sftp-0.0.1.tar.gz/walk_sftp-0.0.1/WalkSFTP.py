import os
import pickle
import pysftp
from base64 import decodebytes
import paramiko
import numpy as np
import datetime as dt
import warnings
from time import sleep
import multiprocessing as mp
from threading import Thread
import pandas as pd
import tempfile
from socket import error as socket_error
from logging import log
warnings.filterwarnings('ignore')

class _FastTransport(paramiko.Transport):
    def __init__(self, sock):
        super(_FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)

class WalkSFTP:
    
    def list_path(self, x):
        try:
            return self._sftp.listdir(x)
        except:
            sleep(60)
            self.connect_sftp()
            return self._sftp.listdir(x)
        
    def check_in_log(self, f, stat_mtime):
        '''
        return True if run ftp download
        '''
        log = self.log_data
        if log == {}: 
            return True
        
        log_file_entry = log.get(f, {})
        if log_file_entry == {}:
            self.class_print('log empty for {} - glob sftp. Running Normal'.format(f))
            return True
        else:
            
            # check if successful get
            if log_file_entry.get('get', False):
                # successful get
                
                if log_file_entry.get('mtime') == stat_mtime:
                    # successful mtim
                    
                    if callable(self.processing_function):
                        # is a process
                        if log_file_entry.get('process', False):
                            self.class_print('Not pulling {} - it is in the log'.format(f))
                            return False
                        else:
                            self.class_print('pulling {} - did not process correctly'.format(f))
                            return True
                            
                    else:
                        self.class_print('Not pulling {} - it is in the log'.format(f))
                        return False
                            
                    
                else:
                    self.class_print('mtime does not match for {} log: {} current: {}'.format(
                        f, log_file_entry.get('mtime'), stat_mtime
                    ))
                    return True
                    
                
            else:
                self.class_print('sftp get did not work {}'.format(f))
                return True
            
        
    def glob_sftp(self, store_paths = ''):
        
        if self._glob_count > self.args.get('break_count', np.inf): 
            return None
        
        for f in self.list_path(store_paths):
            
            new_fp_or_file = os.path.join(store_paths, f)
            stat_bool, stat_mtime = self.test_file(new_fp_or_file)
            stat_mtime = str(stat_mtime)
            if stat_bool:
                
                date_filter = (pd.to_datetime(stat_mtime) >= pd.to_datetime(self.start_date)) and (pd.to_datetime(stat_mtime) <= pd.to_datetime(self.end_date) )
                
                
                if date_filter and self.check_in_log(new_fp_or_file, stat_mtime):
                    self.class_print('{} {} {}'.format(stat_mtime, new_fp_or_file, date_filter))
                    self._glob_count+=1
                    self.q.put(new_fp_or_file)
                    
                if self._glob_count > self.args.get('break_count', np.inf):
                    self.class_print('publishing glob break')
                    self.q.put('break')
                    return None
                
                
            else:
                block = False
                for b in self.blocks:
                    if b in new_fp_or_file:
                        block=True
                        break
                        
                if not block:
                    self.glob_sftp(new_fp_or_file)
                    
        if store_paths == self.orig_store_paths:
            self.class_print('publishing glob break')
            self.q.put('break')
    
    def test_file(self, f):
        for i in range(0, 2):
            try:
                
                stat = self._sftp.stat(f)
                stat_mtime = pd.to_datetime(stat.st_mtime*10e8)
                stat_bool = not stat.st_size is None
                return stat_bool, stat_mtime
            except:
                self.connect_sftp()
        
        return False
    
    def store_all_sftp(self):
        break_count = self.args.get('break_count',np.inf)
        count=0
        while True:
            
            fp = self.q.get()
            
            if isinstance(fp, str) and fp == 'break' or (count>break_count):
                self.class_print('publishing process break')
                self.process_q.put(('break', 'break'))
                break
                
            elif fp is None:
                sleep(1)
            
            elif isinstance(fp, str):
                count+=1
                self.class_print('storing: {}'.format(fp))
                self.store_sftp(fp)
                
                
            self.class_print('.........')
            
            
        self.class_print('finished get function')
        
    def store_sftp(self, fp):
        
        store_path = os.path.join(self._output_path, os.path.dirname(fp))
        store_file = os.path.join(self._output_path, fp)

        if not os.path.exists(store_path):
            os.makedirs(store_path)
        
        if not os.path.exists(store_file):
            try:
                self.get(fp, store_file)
            except Exception as e:
                print('ERROR ON: {} {}'.format(fp, store_file))
                print(e)
                            
    def exit_q(self):
        self.process_q.put(('break', 'break'))
        self.q.put('break')
        self.cleanup()
        
    def connect_sftp(self, returns=False):
        count = 0
        error_connecting, e = True, None
        if returns:
            while True:
                count+=1
                try:
                    transport = _FastTransport((self._base_url, self._port))
                    transport.connect(username = self._username, password = self._password)
                    sftp = paramiko.SFTPClient.from_transport(transport)

                    s = pysftp.Connection(
                        host=self._base_url, 
                        username=self._username, 
                        password=self._password, 
                        cnopts=self.cnopts
                    )
                    error_connecting = False
                    return sftp, s
                
                except Exception as e:
                    
                    sleep(60)
                    if count>10: 
                        self.exit_q()
                        raise ValueError('TOO MANY RETRIES TO CONNECT TO SFTP')
        else:
            transport = _FastTransport((self._base_url, self._port))
            transport.connect(username = self._username, password = self._password)
            self._sftp = paramiko.SFTPClient.from_transport(transport)

            self._s = pysftp.Connection(
                host=self._base_url, 
                username=self._username, 
                password=self._password, 
                cnopts=self.cnopts
            )
            return None
            
        print(f'ERROR: {e}')
        
    def cleanup(self):
        self._sftp.close()
        self._s.close()
        
        if self.close_temporary_directory:
            self.tmpdir.cleanup()
    
    def get(self, remotepath, file):
        count=0
        successful_get = False
        sftp = self._sftp
        start_time = pd.datetime.now()
        
        for i in range(0,2):
            
            sftp, s = self.connect_sftp(True)
            self.class_print(f'starting store get {remotepath}')
            
            try:
                
                stat = sftp.stat(remotepath)
                stat_mtime = str(pd.to_datetime(stat.st_mtime*10e8))
                
                #if self.validate(remotepath, stat_mtime):
                
                s.get(remotepath, file)                   
                self.class_print(f'finished _s get {remotepath}')
                successful_get=True
                self.add_log(remotepath,'get',successful_get)
                self.add_log(remotepath,'mtime', stat_mtime)
                self.add_log(remotepath, 'stat', stat)
                    
                sftp.close()
                s.close()
                    
                break
                
            except Exception as e: 
                self.class_print(remotepath)
                self.class_print(e)
                self.connect_sftp()
        
        if count > 0: sftp.close()
        if not successful_get and os.path.exists(file): os.remove(file)
        assert successful_get, '{} failed'.format(file)
        self.class_print('successful sftp pull {} seconds'.format( int((pd.datetime.now()-start_time).total_seconds()) ))
        
        if callable(self.processing_function): 
            self.process_q.put((file, remotepath))
            
    def class_print(self, msg):
        if self.print_out:
            print(pd.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+' '+str(msg))
            
    
    def main(self):
        
        self.q = mp.Queue()
        self.process_q = mp.Queue()
        
        self.connect_sftp()
        
        glob_thread = Thread(target=self.glob_sftp, name = 'glob')
        glob_thread.start()
        
        store_thread = Thread(target=self.store_all_sftp, name='store')
        store_thread.start()
        
        if callable(self.processing_function): 
            process_thread = Thread(target=self.process_all_ftp, name='process')
            process_thread.start()
        
        
        while True:
            if self.join_threads:
                self.class_print('joining glob thread')
                glob_thread.join()
                self.class_print('joining store thread')
                store_thread.join()
                
                if callable(self.processing_function): 
                    self.class_print('joining process thread')
                    process_thread.join()
                    
                break
                
            #self.class_print('END ---- did not join threads ')
        
    def process_all_ftp(self):
        break_count = self.args.get('break_count',np.inf)
        count=0
        
        while True:
            
            
            fname = self.process_q.get()
            self.class_print('process all ftp finished get {}'.format(fname))
            
            if fname is None:
                self.class_print('SLEEPING')
                sleep(1)
                
                
            elif isinstance(fname[0], str) and fname[0] != 'break':
                count+=1
                successful_process = self.processing_function(fname[0])
                self.add_log(fname[1], 'process', successful_process)
                self.class_print(f'process count is {count}')
                
            elif (isinstance(fname[0], str) and fname[0] == 'break') or (count>break_count):
                self.class_print('JOINING THREADS')
                self.join_threads = True
                return None
                
                
    
    def write_log(self):
        fp = self.log
        if not os.path.exists(os.path.dirname(fp)):
            os.makedirs(os.path.dirname(fp))
            
        pickle.dump(self.log_data, open(self.log, mode='wb'))
    
    def add_log(self, fp, key, value):
        if not fp in self.log_data:
            self.log_data[fp] = {}
        
        self.log_data[fp][key] = value
    
    def read_log(self):
        if self.log is None:
            self.log_data = {}
            
        elif os.path.exists(self.log):
            self.log_data = pickle.load(open(self.log, mode='rb'))
            
        else:
            self.log_data = {}
    
    
    def __init__(
        self, 
        base_url, 
        username,
        password,
        port=22,
        store=None, 
        processing_function=None,
        log=None,
        blocks=[],
        start_date = pd.to_datetime('1970-01-01'),
        end_date = pd.datetime.today()+dt.timedelta(1),
        **args,
    ):
        '''
        Parameters
        ----------
        base_url : str
            URL that you are pulling the SFTP
        username : str
            Username to login to the SFTP
        password : str
            Username to login to the SFTP
        port : int
            port
        store : None, str
            Path after to store files. If None, then 
            stores in a temporary directory. Use with
            1) processing_function argument to get 
            data from them and a log filepath to keep
            track of files already downloaded
        processing_function : None/function
            pass function if you want to process the 
            data after sftp pull. Takes teh filepath as an
            argument. Returns True/False depending on whether
            the process ran correctly
        log : str
            filepath of log to get information on data.
            This can be used for a temporary directory
            in order to not keep the files stored but 
            know that the data is processed. Should be
            a .p file
        blocks : list
            list of str to block. Looks for string
            in file path of each entry in blocks
            to determine whether to pull
        start_date : str/datetime
            date to only pull files that were modified after
            this date - default 1970-01-01
            
        Optional Args
        -------------
        print_out : bool
            Whether to print out messages (slower when True)
        break_count : int
            stop running sftp download after n number of files downloaded
        '''
        self.args=args
        self._glob_count=0
        print_out = args.get('print_out', False)
        
        if isinstance(blocks, str):
            blocks = [blocks]
            
        self.blocks = blocks
        self.print_out = print_out
        
        if not store is None:
            self.class_print(f'store is not None: {store}')
            self._output_path = store
            self.close_temporary_directory = False
        else:
            self.close_temporary_directory = True
            self.tmpdir = tempfile.TemporaryDirectory()
            self._output_path = self.tmpdir.name
            self.class_print(f'temporary directory {self._output_path}')
            
        self.log = log
        self.read_log()
        self.join_threads = False
        
        self._username = username
        self._password = password
        self._port=port
        self._base_url = base_url
        self.processing_function = processing_function
        self.file_list = []
        self.orig_store_paths = ''
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.create_pysftp_host_key()
        self.run()
        if log != None: self.write_log()
        
    def run(self):
        self.main()
        self.cleanup()
        
        
    def create_pysftp_host_key(self):
        ssh_key = os.popen('ssh-keyscan {}'.format(self._base_url)).read().split(' ')
        self.cnopts = pysftp.CnOpts()
        
        keydata = ssh_key[2].encode()
        key = paramiko.RSAKey(data= decodebytes(keydata))
        self.cnopts.hostkeys.add(ssh_key[0],ssh_key[1],key)
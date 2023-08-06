# WalkSFTP

This is project is a class that allows for a glob like sftp download to a temporary file and lets you process the downloaded data using processing_function. The log argument can be used to check if the get and process ran correctly so you can run and not pull files that have already been processed and keeps track of files based on their modified time. This uses threading to separate the glob sftp files and the process function.

## Installation

Run the following to install: 

```python
pip install walk_sftp
```

## Usage

```
from walk_sftp import WalkSFTP

def process(f)
	
	try:
		# if successfull
		return True
	except:
		# if unsuccessfull
		return False

WalkSFTP(
    ftp_web_address,
    username,
    password,
    start_date='2020-12-25', # optional
	end_date='2020-12-28', # optional
    print_out=True, # optional
    processing_function=process, # optional
    log='/some_path_to_log.p', # optional
)
```

## Development walk_sftp

To install walk_sftp, along with the tools you need to develop and run tests, run the following in your virtualend:
```bash
$ pip install -e .[dev]
```

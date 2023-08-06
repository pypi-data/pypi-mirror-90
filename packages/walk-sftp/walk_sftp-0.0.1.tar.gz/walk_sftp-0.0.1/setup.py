from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author='Christopher Bell',
    author_email='Chris.E.Bell24@gmail.com',
    maintainer='Christopher Bell',
    maintainer_email='Chris.E.Bell24@gmail.com',
    url='https://github.com/chrisebell24/walk_sftp',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    name='walk_sftp',
    version='0.0.1',
    description='Download SFTP files using a glob to get all files & also keep a log to keep track of processing',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[],
    package_dir={'': 'src'},
    install_requires = [
        "numpy>=1.16.1",
        "pysftp>=0.2.9",
        "paramiko>=2.7.2",
    ],
    extras_require = {
        "dev": [
            "pytest >= 3.7",
        ],
    },
)
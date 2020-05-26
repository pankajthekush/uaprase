
from setuptools import setup,find_packages
from subprocess import check_call
from glob import glob
import os
import sys
current_path  = os.path.dirname(os.path.realpath(__file__))


setup(
    name='uaparse',
    version='1.3',
    packages=['uaparse'],
    install_requires=['SQLAlchemy>=1.3.16','beautifulsoup4>=4.9.0','ua-parser>=0.10.0'],
    entry_points ={'console_scripts': ['parseupload = uaparse.parseua:parse_upload',
                                        'parseonly = uaparse.parseua:ua_from_html',
                                        'uploadonly=uaparse.parseua:insert_to_db']} 
)
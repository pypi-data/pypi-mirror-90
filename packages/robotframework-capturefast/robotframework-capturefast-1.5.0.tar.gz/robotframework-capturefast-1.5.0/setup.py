from distutils.core import setup
from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_descriptions = f.read()
    
setup(
    name = 'robotframework-capturefast',
    packages = ['.'],
    version = '1.5.0',
    description = 'Capturefast Bridge Library For Robocorp',
    author = 'CaptureFast',
    author_email = 'support@capturefast.com',
    url = 'https://github.com/CaptureFastSupport/CaptureFastForRobocorpLibrary',
    keywords = ['OCR', 'Capture','Document','Parser','RPA'],
    requires = ['robotframework', 'six'],
    long_description=long_descriptions,
    long_description_content_type='text/markdown'
)
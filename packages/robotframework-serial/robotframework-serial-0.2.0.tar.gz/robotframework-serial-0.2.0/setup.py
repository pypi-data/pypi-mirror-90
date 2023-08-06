#!/usr/bin/env python

from os.path import abspath, dirname, join
from sys import platform


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if platform.startswith('java'):
    try:
        import javax.comm
    except ImportError:
        print ('Remember, PySerial on Jython requires java.comm.')


CURRENT_DIR = dirname(abspath(__file__))

with open(join(CURRENT_DIR, 'src', 'Serial', 'version.py')) as f:
    exec(f.read())
    VERSION = get_version()

README = open(join(CURRENT_DIR, 'README.rst')).read()
CLASSIFIERS = '\n'.join(
    map(' :: '.join, [
        ('Development Status', '3 - Alpha'),
        ('License', 'OSI Approved', 'Apache Software License'),
        ('Operating System', 'OS Independent'),
        ('Programming Language', 'Python', '3.9'),
        ('Topic', 'Software Development', 'Testing'),
    ])
)

setup(
    name='robotframework-serial',
    version='.'.join(map(str, VERSION)),
    description='Robot Framework test library for serial connection',
    long_description=README,
    author='Fredrik Karlsson',
    author_email='f.v.carlsson@gmail.com',
    url='https://github.com/Warcaith/robotframework-serial',
    license='Apache License 2.0',
    keywords='robotframework testing testautomation serial',
    platforms='any',
    classifiers=CLASSIFIERS.splitlines(),
    package_dir={'': 'src'},
    packages=['Serial'],
    install_requires=['robotframework', 'pyserial'],
)
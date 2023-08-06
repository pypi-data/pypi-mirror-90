from setuptools import find_packages, setup
from io import open as io_open
from os import path

here = path.abspath(path.dirname(__file__))


def readall(*args):
    with io_open(path.join(here, *args), encoding="utf-8") as fp:
        return fp.read()


documentation = readall("Readme.md")

setup(
    name='postbot',
    packages=['postbot'],
    version='0.1.4',
    description='A simple tool to make posts on Instagram programmatically',
    long_description=documentation,
    long_description_content_type="text/markdown",
    author='Tom G',
    url='https://github.com/GAtom22/postbot',
    download_url='https://github.com/GAtom22/postbot/archive/0.1.4.tar.gz',
    license='GPLv3',
    keywords=(
        "postbot python instagram post automation \
         marketing promotion bot selenium"
    ),
    install_requires=["selenium>=3.141.0", "mysql-connector-python>=8.0.22"],
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    platforms=["win32", "linux", "linux2", "darwin"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)

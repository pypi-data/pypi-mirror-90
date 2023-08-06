import setuptools

import versioneer

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name = "stringtopy",
    version = versioneer.get_version(),
    packages = setuptools.find_packages(),
    install_requires = [],
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "stringtopy is a small library to convert strings to a specified type (e.g. int, float or bool), allowing more human friendly input similar to configparser.",
    long_description = long_description,
    long_description_content_type='text/markdown',
    license = "3-clause BSD",
    keywords = "strings",
    url = "http://stringtopy.rtfd.io",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass=versioneer.get_cmdclass(),
)

import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-filemetadata",
    version="1.0.3",
    author="Rodrigo Ristow",
    author_email="rodrigo@maxttor.com",
    description="Synchronize the metadata from local files in the DB",
    license="BSD",
    keywords="django file metadata",
    url="https://gitlab.com/rristow/django-filemetadata",
    packages=find_packages(),
    data_files=[
            ('output_dir', ['tests/*']),
        ],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

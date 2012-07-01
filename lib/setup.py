#!/usr/bin/env python
#
########################################################################################
#  2011 by Josef Kral                                                                  #
#                                                                                      #
#  Original application is Cdcatfs by Dorin Scutara\u015fu <dorin.scutarasu@gmail.com> #
#                                                                                      #
#  This program is free software; you can redistribute it and/or modify                #
#  it under the terms of the GNU General Public License. See the file                  #
#  COPYING for details.                                                                #
########################################################################################

from distutils.core import setup
import sys

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords. Needed for python < 2.2.3.
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None


#there must be a better way to do this
if version < '2.4':
    raise RuntimeError('You need python-2.4 or newer.')

try:
    import fuse
except ImportError:
    raise RuntimeError("You need python-fuse (and pysqlite2) installed. Please install "
                       ">=fuse-python-2.0 and try again.")

try:
    from pysqlite2 import dbapi2
except ImportError:
    raise RuntimeError("You need have pysqlite (and python-fuse) installed. Please install "
            "it and try again.")


if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-python doesn't know of fuse.__version__, "
        "probably it's too old.")


scatfs_classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)'
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Topic :: Database :: Front-Ends',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'
        ]


setup(name='scatfs',
    version='0.1.0',
    description='Catalog Filesystem using FUSE',
    long_description=\
''' Scatfs (Catalog Filesystem) is a tool that allows one to create a
file catalog from a mounted (or otherwise any directory) and later
mount that catolog and explore it. The program provide mapping of
number of catalogized files onto st_nlink file attribute. The catalog
is stored as a SQLite database and the filesystem is implemented using
FUSE.''',
    author='Dorin Scutarasu',
    author_email='dorin.scutarasu@gmail.com',
    license='GNU General Public License (GPL)',
    url='http://students.infoiasi.ro/~dorin.scutarasu/scatfs/',
    download_url='http://students.infoiasi.ro/~dorin.scutarasu/scatfs/scatfs-0.1.5.tar.gz',
    package_dir={'' : 'src'},
    packages=['Scatfs'],
    scripts=['src/scatman','src/scatfs'],
    classifiers=scatfs_classifiers
    )

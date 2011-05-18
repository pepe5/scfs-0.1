# use: cd /home/user/text/scfs; ruby lib/test/scfs-fun.rb
import os
import re
import shutil
import shlex
import subprocess
import sys
from stat import *

class Config:
    wd = '/tmp/dev/scwd'
    @classmethod
    def load(self):
        self.oldwd = os.getcwd()
        os.chdir(self.wd)
    @classmethod
    def unload(self):
        os.chdir(self.oldwd)

def scatfs(argstr):
    argstr = os.path.expanduser(argstr)
    args = shlex.split(argstr)
    Config.mounto = args [-1]
    print " -vfs mount point: %s" % Config.mounto
    Config.db = re.match('.*database=([^ ]+) ', argstr).group(1) # @KNOWN as not-universal
    Config.db = os.path.expanduser(Config.db)
    print " -registering (blind dir) at: %s" % Config.wd
    wdtbl = 'WD_UC1'
    print " -into arch.fld: %s" % wdtbl
    cmd = 'cdcatman del %s %s' % (wdtbl, Config.db)
    pop = subprocess.Popen(shlex.split(cmd))
    print " -cleaning wd table: %s" % cmd
    cmd = 'cdcatman add %s %s %s' % (Config.wd, wdtbl, Config.db)
    pop = subprocess.Popen(shlex.split(cmd))
    print " -adding wd table: %s" % cmd

def echo(data, **kwargs):
    of = file(kwargs['ofile'], 'w')
    of.write(data)
    of.close()

def cap(wd):
    cmd = '/usr/bin/find . -type f -ls'
    pop = subprocess.Popen(shlex.split(cmd))
    print " -capturing wd state: \%s" % cmd

##
# @brief 1/Register (testing) wd, 2/Add mockup, 3/Check duplical file/s
def test_uc1():
    '''Use case 1'''
    Config.load()
    scatfs('-s -o database=~/.scfs/cat1.db ~/mnt/cat1')
    echo('123', ofile='a/123')
    echo('321', ofile='a/321')
    echo('123', ofile='b/123')
    f123 = {}; f123['st_nlink'] = os.stat('a/123')[ST_NLINK]
    cap('.')
    assert f123['st_nlink'] == 2
    Config.unload()

def like_tc2():
    ''' Check add around broken links:
    scfs> cdcatman add . CD_1 ~/.scfs/cat1.db
    -Error: [Errno 2] No such file or directory: '/home/p-b/text/scfs/lib/Cdcatfs~' '''
    pass

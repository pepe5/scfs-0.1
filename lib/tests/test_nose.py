# use: cd /home/user/text/scfs; ruby lib/test/scfs-fun.rb
import os
import re
import shutil
import shlex
import subprocess
import sys
from stat import *

class ConfigDict(dict):
    def load(self, **kwargs):
        if not 'oldwd' in self:
            self['oldwd'] = []
        self['oldwd'].append(os.getcwd())
        if not 'wd' in self:
            self['wd'] = []
        self['wd'] = kwargs['wd']
        os.chdir(kwargs['wd'])

    def unload(self):
        self['wd'] = self['oldwd'].pop()
        os.chdir(self['wd'])

Config = ConfigDict()

def scatfs(argstr):
    argstr = os.path.expanduser(argstr)
    args = shlex.split(argstr)
    Config.mounto = args [-1]
    print " -vfs mount point: %s" % Config.mounto
    Config.db = re.match('.*database=([^ ]+) ', argstr).group(1) # @KNOWN as not-universal
    Config.db = os.path.expanduser(Config.db)
    print " -registering (blind dir) at: %s" % Config['wd']
    Config.adname = 'WD_UC1'
    print " -into arch.fld: %s" % Config.adname
    cmd = 'cdcatman del %s %s' % (Config.adname, Config.db)
    pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    print " -cleaning wd table: %s" % pop.communicate()[0]
    cmd = 'cdcatman add %s %s %s' % (Config['wd'], Config.adname, Config.db)
    pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    print " -adding wd table: \n%s" % pop.communicate()[0]

def echo(data, **kwargs):
    of = file(kwargs['ofile'], 'w')
    of.write(data)
    of.close()

def cap(wd):
    cmd = '/usr/bin/find . -type f -ls'
    pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    print " -capturing wd state: \n%s" % pop.communicate()[0]

##
# @brief 1/Register (testing) wd, 2/Add mockup, 3/Check duplical file/s
def test_uc1():
    '''Use case 1'''
    srcd = '/tmp/dev/scwd'
    outroot = os.path.expanduser('~/mnt/cat1')
    Config.adname = 'WD_UC1'

    Config.load(wd=srcd)
    scatfs('-s -o database=~/.scfs/cat1.db ~/mnt/cat1')
    echo('123', ofile='a/123')
    echo('321', ofile='a/321')
    echo('123', ofile='b/123')
    Config.unload()

    Config.load(wd=outroot)
    print ' -pwd.. %s' % os.getcwd()
    f123 = {}; f123['st_nlink'] = os.stat(Config.adname + '/a/123')[ST_NLINK]
    cap('.')
    assert f123['st_nlink'] == 2
    Config.unload()

def like_tc2():
    ''' Check add around broken links:
    scfs> cdcatman add . CD_1 ~/.scfs/cat1.db
    -Error: [Errno 2] No such file or directory: '/home/p-b/text/scfs/lib/Cdcatfs~' '''
    pass

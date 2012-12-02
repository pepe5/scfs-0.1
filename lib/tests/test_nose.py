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
Config.srcd = '/tmp/dev/scwd'
Config.outroot = os.path.expanduser('~/mnt/cat1')
Config.db = os.path.expanduser('~/.scfs/cat1.db')

def scatman(argstr, **kw):
    '''Runs scatman command-line
    optional @param kw['mountPoint'] can override default Config['wd']
    optional @param kw['cont'] suppresses setup refreshment of the Table
    '''
    argstr = os.path.expanduser(argstr)
    args = shlex.split(argstr)
    if 'mountPoint' in kw:
        mountPoint = kw['mountPoint']
        print " -mountPoint redefined: %s" % mountPoint
    else:
        mountPoint = Config['wd']

    Config.mounto = args [-1]
    print " -vfs mount point: %s" % Config.mounto
    Config.db = re.match('.*database=([^ ]+) ', argstr).group(1) # @KNOWN as not-universal
    Config.db = os.path.expanduser(Config.db)
    print " -registering (blind dir) at: %s" % Config.db
    Config.adname = 'WD_UC1'
    print " -into arch.fld: %s" % Config.adname

    if not 'cont' in kw:
        cmd = 'scatman del %s %s' % (Config.adname, Config.db)
        pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        print " -cleaning wd table: %s" % pop.communicate()[0]

    cmd = 'scatman add %s %s %s' % (mountPoint, Config.adname, Config.db)
    pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    print " -adding wd table: \n%s" % pop.communicate()[0]

def echo(data, **kwargs):
    '''echo like utility'''
    of = file(kwargs['tofile'], 'w')
    of.write(data)
    of.close()

def mkdirp(*args):
    '''mkdir like utility'''
    for d in args:
        try:
            os.makedirs(d)
        except OSError, err:
            print " -makedirs exception: %s" % err

def capture(path):
    '''lists working dir content'''
    cmd = '/usr/bin/find %s -type f -ls' % path
    pop = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    print " -capturing overview of path: %s \n%s" % (os.path.abspath(path), pop.communicate()[0])

def test_uc0z():
    '''Smoke Test
    @brief 1/Add dir/s stru, 2/Mount FS
    '''
    mkdirp(os.path.join(Config.srcd, 'a'), os.path.join(Config.srcd, 'b'))
    mkdirp(os.path.join(Config.outroot, Config.db))

def test_uc1z():
    '''Use case 1
    @brief 1/Register (testing) wd, 2/Add mockup, 3/Check duplical file/s'''
    Config.adname = 'WD_UC1'

    Config.load(wd=Config.srcd)
    echo('123', tofile='a/123')
    echo('321', tofile='a/321')
    echo('123', tofile='b/123')
    scatman('-s -o database=~/.scfs/cat1.db ~/mnt/cat1')
    Config.unload()

    Config.load(wd=Config.outroot)
    f123 = {}
    f123['st_nlink'] = os.stat(Config.adname + '/a/123')[ST_NLINK]
    capture('.')
    print " -got nlink: %s ( -exp: %s )" % (f123['st_nlink'], 2)
    assert f123['st_nlink'] == 2
    Config.unload()

def test_uc1 ():
    '''Use case 1 (Catalog for xattrs)
    @brief 1/Add 2files, 2/Ins.them, 3/Ls.theirs xattrs'''
    Config.adname = 'WD_UC1'
    Config.load (wd = Config.srcd)
    echo ('123', tofile = 'a/123')
    echo ('234', tofile = 'b/bb/234')
    scatman ('-s -o database=~/.scfs/cat1.sqlite')
    scatxattrs ('-i database=~/.scfs/cat1.sqlite')
    capture ('.', xattrs='user.*')
    Config.unload()

def test_uc2z():
    '''Use case 2
    @brief 1/UC1, 2/Add Insertion, 3/Check tree graph'''
    Config.adname = 'WD_UC1'

    Config.load(wd=Config.srcd)
    userPoint = os.path.join(Config.srcd, 'b', 'bb')
    mkdirp(userPoint, os.path.join(userPoint, 'bbb'))
    echo('234', tofile='b/bb/bbb/234')
    scatman('-s -o database=~/.scfs/cat1.db ~/mnt/cat1',
            mountPoint = userPoint,
            cont=True)
    Config.unload()

    Config.load(wd=Config.outroot)
    print 'pep> -pwd: %s' % os.getcwd()
    dbbb = os.listdir(os.path.join(Config.adname, 'b/bb/bbb'))
    capture('.')
    print " -got in bbb: %s" % (dbbb)
    assert dbbb == ['234']
    Config.unload()

def like_tc_l2():
    ''' Check add around broken links:
    scfs> scatman add . CD_1 ~/.scfs/cat1.db
    -Error: [Errno 2] No such file or directory: '/home/p-b/text/scfs/lib/Cdcatfs~' '''
    pass

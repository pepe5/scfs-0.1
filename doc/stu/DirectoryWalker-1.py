# use: $0 dir [startAt=dir/2 parentId=3 lastId=7]
import sys
from Scfs.DirectoryWalker import DirectoryWalker

basedir = '/tmp/dev/scwd/'
if len (sys.argv) > 1:
    basedir = sys.argv[1]
print ' -basedir: %s' % basedir

kw = dict((k,v) for k,v in (kv.split('=') for kv in sys.argv[2:]))
opts = {}
for k,v in kw.iteritems():
    try:
        opts[k] = int(v)
    except ValueError:
        opts[k] = v
print ' -opts: %s' % opts

for (fname,stats,fileId,parentId) in DirectoryWalker (basedir,opts):
  print fileId, parentId, fname

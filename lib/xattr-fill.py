# test:$> (cd /tmp/dev/scwd/; ls -1 a) | (python -u lib/xattr-fill.py)

import os
import sys
from pysqlite2 import dbapi2 as sqlite

dbfile = os.path.expanduser ('~/.scfs/cat1.cdcat')
if not os.path.exists (dbfile):
    raise ValueError ('Database not found.')
con = sqlite.connect (dbfile)
cur = con.cursor ()

cdlabel = 'WD_UC2'

while 1:
    try:
        filename = sys.stdin.readline () .rstrip ()
    except KeyboardInterrupt:
        break

    if not filename:
        break

    cur.execute \
        ("select * from %s where fileName = '%s'" %
         (cdlabel+'_files', filename))
    row1 = cur.fetchall () [0]
    rowd = {}
    for k,v in zip (('fid',
         'pid',
         'fileName',
         'st_mode',
         'st_nlink',
         'st_uid',
         'st_gid',
         'st_size',
         'st_atime',
         'st_mtime',
         'st_ctime'), row1):
        rowd [k] = v
        if k != 'fid':
            print '''setfattr -n user.scfs.%s.%s.%s -v "%s"''' %\
                (cdlabel,rowd['fid'], k,v)
    # print 'attr/s of %s: %s' % (filename,rowd)

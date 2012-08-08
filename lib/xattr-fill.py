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
    rows = cur.fetchall()
    print 'attr/s of %s: %s' % (filename,rows)

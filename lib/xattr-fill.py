import os
import sys
from pysqlite2 import dbapi2 as sqlite

filename = 'a'

dbfile = os.path.expanduser ('~/.scfs/cat1.sqlite')
if not os.path.exists (dbfile):
    raise ValueError ('Database not found.')
con = sqlite.connect (dbfile)
cur = con.cursor ()

cdlabel = 'WD_UC2'
cur.execute \
    ("select * from %s where fileName = '%s'" %
     (cdlabel+'_files', filename))

rows = cur.fetchall()
print 'attr/s of %s: %s' % (filename,rows)

# while 1: 
#    try:
#         line = sys.stdin.readline ()
#     except KeyboardInterrupt:
#         break

#     if not line:
#         break

#     print line

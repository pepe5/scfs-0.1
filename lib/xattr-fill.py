import os
import sys
from pysqlite2 import dbapi2 as sqlite

dbfile = os.path.expanduser ('~/.scfs/cat1.sqlite')
cdlabel = 'WD_UC2'
if not os.path.exists (dbfile):
    raise ValueError ('Database not found.')
con = sqlite.connect (dbfile)
cur = con.cursor ()
cur.execute ("select fid,label from CDs where label = '%s'" % cdlabel)
rows = cur.fetchall()
print 'label: fid: %s' % rows

# while 1: 
#    try:
#         line = sys.stdin.readline ()
#     except KeyboardInterrupt:
#         break

#     if not line:
#         break

#     print line

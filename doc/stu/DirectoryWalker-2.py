from Scfs.DirectoryWalker import DirectoryWalker
for (fname,stats,fileId,parentId) in DirectoryWalker ('/tmp/dev/scwd',
    {'startAt':['bb'], 'parentId':2, 'lastId':6, 'startAbs':'/tmp/dev/scwd/b/bb'}):
  print fileId, parentId, fname

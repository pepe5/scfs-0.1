#!/usr/bin/env python
#
###########################################################################
#  Copyright (C) 2006 by Dorin Scutara\u015fu <dorin.scutarasu@gmail.com> #
#                                                                         #
#  This program is free software; you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License. See the file     #
#  COPYING for details.                                                   #
###########################################################################

import os,stat,sys
from stat import *

from pysqlite2 import dbapi2 as sqlite

from ScatServices import *
from DirectoryWalker import DirectoryWalker
from utils import ConsoleSpinner


class CatalogCreator:
    ''' stores metadata of files in a directory tree in a SQLite database
    '''
    tableName = "files"

    def __init__(self,dbFile,mountPoint,CDLabel):
        self.__dbFile = dbFile        
        #TODO:test if file exists and create if necessary
        if not os.path.exists(mountPoint) :
            raise OSError,"MountPoint not accesible."
        self.__mountPoint = os.path.realpath(mountPoint)
        self.__CDLabel = CDLabel
        self.__initDb();
        self.__spinner = ConsoleSpinner();

    def run(self):
        con = sqlite.connect(self.__dbFile)
        cur = con.cursor()

        walkerKwargs = {}
        if self.middleid:
            walkerKwargs['startAt'] = ***

        for (fileName,stats,fileId,parentId) in\
                            DirectoryWalker(self.__mountPoint):

            if(stat.S_ISDIR(stats[ST_MODE])):
                self.__spinner.update()
            st_mode = stats[0]
            st_nlink = stats[3]
            st_uid,st_gid = stats[4:6]
            st_size = stats[6]
            st_atime,st_mtime,st_ctime = stats[7:]
            
            cur.execute("INSERT OR REPLACE INTO %s_files "\
            "(fid,pid,fileName,st_mode,st_nlink,st_uid, "\
            "st_gid,st_size,st_atime,st_mtime,st_ctime) "\
            "VALUES (?,?,?,?,?,?,?,?,?,?,?);" %self.__CDLabel,\
            (fileId,parentId,fileName,st_mode,st_nlink,st_uid,\
            st_gid,st_size,st_atime,st_mtime,st_ctime))
        self.__spinner.clean()
        con.commit()

    def __initDb(self):
        con = sqlite.connect(self.__dbFile)
        cur = con.cursor()

        self.startAt = None

        try:
            cur.execute("select * from CDs where label = '%s'" % self.__CDLabel);
            rows = cur.fetchall()
            if len(rows)>0 :
                
                sys.stdout.write("Label exists. Trying add onto existing mountPoint\n")
                self.startAt = self.__mountPoint
                server = CDCatFS(version="%prog " + fuse.__version__,
                     usage='', dash_s_do='setsingle')
                server.connect(database=self.__dbFile)
                self.middleid = 1
                pathComponents = server.splitPath(self.__mountPoint)
                newMountPoint = []
                for name in pathComponents:
                    pidTry = server.getId(name, self.middleid, self.__CDLabel)
                    if pidTry > -1:
                        self.middleid = pidTry
                    else:
                        break
                self.__mountPoint = 
                sys.stdout.write(" - in -mountPoint:.. -exists-path(%s):.. so we "\
                                 "will continue -adding:.. \n" % self.middleid)

        except sqlite.OperationalError:
            pass
        
        statement = "CREATE TABLE IF NOT EXISTS CDs( "\
            "fid integer primary key autoincrement,"\
            "label text); "
        cur.execute(statement)
        statement = "INSERT INTO CDs (label) "\
                 "VALUES('%s');" % self.__CDLabel
        cur.execute(statement)
        
        statement = "CREATE TABLE IF NOT EXISTS %s_files( "\
            "fid integer primary key,"\
            "pid integer,"\
            "fileName text, "\
            "st_mode integer, "\
            "st_nlink integer, "\
            "st_uid integer default 0, "\
            "st_gid integer default 0, "\
            "st_size integer default 0, "\
            "st_atime integer default 0, "\
            "st_mtime integer default 0, "\
            "st_ctime integer default 0);" % self.__CDLabel;
        cur.execute(statement)
        cur.execute('CREATE INDEX IF NOT EXISTS %s_pid_idx ON %s_files( pid );'% (self.__CDLabel,self.__CDLabel))
        cur.execute('CREATE INDEX IF NOT EXISTS %s_fname_idx ON %s_files(fileName);'%(self.__CDLabel,self.__CDLabel))
        cur.execute('CREATE INDEX IF NOT EXISTS %s_pid_fname_idx ON %s_files(pid,fileName);'%(self.__CDLabel,self.__CDLabel))
        con.commit()

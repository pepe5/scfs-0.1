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

        walkerOpts = {}
        if self.startAt:
            walkerOpts['mountPoint'] = self.__mountPoint
            walkerOpts['parentId'] = self.parentId
            walkerOpts['lastId'] = self.lastId
            walkerOpts['startAt'] = self.startAt
            walkerOpts['startAbs'] = self.startAbs
            sys.stdout.write(" -run startAt will be soon..\n")

        for (fileName,stats,fileId,parentId) in\
                            DirectoryWalker(self.__mountPoint, walkerOpts):

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
            cur.execute("select mountPoint from CDs where label = '%s'" % self.__CDLabel);
            rows = cur.fetchall()
            if len(rows)>0 :
                
                self.startAbs = self.__mountPoint
                sys.stdout.write("Label exists. Trying add onto existing mountPoint\n")
                server = CDCatFS(version="%prog " + fuse.__version__,
                     usage='', dash_s_do='setsingle')
                server.connect(database=self.__dbFile)
                self.startAt = server.splitPath(self.__mountPoint) # user (insertion) path
                self.__mountPoint = rows[0][0] # already-archived CD's mountPoint path
                archivedPoint = server.splitPath(self.__mountPoint)
                sys.stdout.write(" - from (common) -mountPoint: %s\n"
                                     % self.__mountPoint)

                if archivedPoint == self.startAt:
                    raise NotImplementedError, "update reload not yet implemented"

                if len(archivedPoint) > len(self.startAt):
                    raise NotImplementedError, "re-indexing extend not yet implemented"

                # find longest common part from archived-Point to user-Point
                self.startAt = self.startAt[len(archivedPoint):]
                hops = 0
                self.parentId = 1
                for name in self.startAt:
                    pidTry = server.getId(name, self.parentId, self.__CDLabel)
                    if pidTry == -1:
                        break
                    else:
                        hops += 1
                        self.parentId = pidTry
                sys.stdout.write(" -last-id from common part: %s\n"\
                                     % (self.parentId))

                self.startAt = self.startAt[hops:]
                cur.execute("select max(fid) from %s_files" % self.__CDLabel);
                self.lastId = cur.fetchall()[0][0]
                sys.stdout.write(" -startPoint: %s, -lastId: %d\n" % (self.startAt, self.lastId))

        except sqlite.OperationalError, err:
            sys.stdout.write(" -got exception at sql execution.. %s\n" % err)
            pass
        
        statement = "CREATE TABLE IF NOT EXISTS CDs( "\
            "fid integer primary key autoincrement,"\
            "label text, mountPoint text); "
        cur.execute(statement)
        statement = ("INSERT INTO CDs (label, mountPoint) " +
            "SELECT '%s', '%s' " +
            "WHERE NOT EXISTS (SELECT 1 FROM CDs WHERE label = '%s');")\
            % (self.__CDLabel, self.__mountPoint, self.__CDLabel)
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

#!/usr/bin/env python
#
###########################################################################
#  Copyright (C) 2006 by Dorin Scutara\u015fu <dorin.scutarasu@gmail.com> #
#                                                                         #
#  This program is free software; you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License. See the file     #
#  COPYING for details.                                                   #
###########################################################################


import os

class DirectoryWalker:
	# a forward iterator that traverses a directory tree, and
	# returns the filename

	def __init__(self, directory, opts={}):
		directory = os.path.abspath(directory)
		self.stack = []
		self.files = [directory]
		self.directory = directory
		self.index = 0
		self.pathPrefix = directory #marked for deletion
		self.prefixLen = len(directory)+1
		self.parentId = 0	#parent id
		self.fileId = 0	#current file id
		self.startId = 1 	#root id

		if 'startAt' in opts: #all following must be supplied in this case
			self.parentId = opts['parentId']
			self.directory = opts['startAbs']
			self.fileId = opts['lastId']
			self.startId = self.fileId+1


	def __getitem__(self, index):
		while True:
			try:
				file = self.files[self.index]
				self.index = self.index + 1
			except IndexError:
			# pop next directory from stack
				self.directory,self.parentId = self.stack.pop()
				self.files = os.listdir(self.directory)
				self.index = 0
			else:
				self.fileId = self.fileId +1
				# get a filename, add directory to stack
				fullname = os.path.join(self.directory, file)
				if os.path.isdir(fullname) : #and not os.path.islink(fullname):
					self.stack.append((os.path.normpath(fullname),self.fileId))
				stats = os.stat(fullname)
				#fullname = fullname[self.prefixLen:]
				#ugly warkaround. It would return the full path of the directory
				#given as parameter
				if(self.fileId == self.startId):
					file = file[self.prefixLen:]
				return (file,stats,self.fileId,self.parentId)

if __name__ == '__main__' :
	d = DirectoryWalker('.')
	for (fname,stats,fileId,parentId) in d:
		print fname, fileId,parentId

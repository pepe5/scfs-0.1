#!/usr/bin/perl -nl
# read file:~/text/scfs/doc/README.org
#>! use as: find . -type f -ls | perl -nl $ARGV[0] > $F.import &
use POSIX;

BEGIN
{ print "PRAGMA foreign_keys=OFF;
      BEGIN TRANSACTION;
      CREATE VIRTUAL TABLE find_ls USING fts4
      ( ix INTEGER PRIMARY KEY AUTOINCREMENT,
        dt DATETIME DEFAULT CURRENT_TIMESTAMP,
        fts4 TEXT
      );"
}

s/'/''/g; 
s/\\([^\\])/$1/g;
print "INSERT INTO find_ls VALUES
      ( NULL,
        '".(strftime "%F %T", localtime)."',
        '$_');";

END { print "COMMIT;" }

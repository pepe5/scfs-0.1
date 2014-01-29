#!/usr/bin/perl -nl
# read file:~/text/scfs/doc/README.org
#>! use as: find . -type f -printf "%i %k %M %n %u %g %s %TY-%Tm-%Td %TH:%TM:%TS %h/%f\n" | perl -nl $0 | pv | sqlite3 $F.sqlite
use POSIX;
BEGIN
{ print "PRAGMA foreign_keys=OFF;
      BEGIN TRANSACTION;
      CREATE TABLE find_printf
      ( ix INTEGER PRIMARY KEY AUTOINCREMENT,
        dt DATETIME DEFAULT CURRENT_TIMESTAMP,
        inode INTEGER,
        du INTEGER,
        perms TEXT,
        lns INTEGER,
        ug TEXT,
        s INTEGER,
        mtime DATETIME,
        dir TEXT,
        fn TEXT);" }
#>! ins. after dt> ut :: unlink-time - when file is moved or unlinked

s/'/''/g;
m{^
    (\d+)\s+		# $1 - iNode
    (\d+)\s+		# $2 - Occupation (kB)
    (\S+)\s+		# $3 - Permissions (([\w-.+@]+) is not enough for AIX)
    (\d+)\s+		# $4 - Links #
    (\w+\s+\w+)\s+	# $5 - User + Group
    (\d+)\s+		# $6 - Size (B)
    ([\d-]+\s+[\d:]+)\.\d+\s+ # $7 - Date + Time (%Y-%m-%d %H:%M:%S.<F>)
    (.*?)		        # $8 - DirName
    ([^/]+)		        # $9 - BaseName
    $}x;

# s/\\([^\\])/$1/g; #< deprecated for find-printf
print "INSERT INTO find_printf VALUES
      ( NULL,
        '".(strftime "%F %T", localtime)."',
        '$1','$2','$3','$4','$5','$6','$7','$8','$9');";

END { print "COMMIT;" }

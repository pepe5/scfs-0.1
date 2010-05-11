BEGIN TRANSACTION;
CREATE TABLE CDs( fid integer primary key autoincrement,label text);
INSERT INTO "CDs" VALUES(1,'aspire1_sda1');
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('CDs',1);
CREATE TABLE aspire1_sda1_files( fid integer primary key,pid integer,fileName text, st_mode integer, st_nlink integer, st_uid integer default 0, st_gid integer default 0, st_size integer default 0, st_atime integer default 0, st_mtime integer default 0, st_ctime integer default 0);
INSERT INTO "aspire1_sda1_files" VALUES(1,0,'',16893,2,500,500,60,1273464827,1272828499,1272828499);
INSERT INTO "aspire1_sda1_files" VALUES(2,1,'personal-developing.file',33204,1,500,500,25,1272827144,1272827144,1272828499);
CREATE INDEX aspire1_sda1_pid_idx ON aspire1_sda1_files( pid );
CREATE INDEX aspire1_sda1_pid_fname_idx ON aspire1_sda1_files(pid,fileName);
COMMIT;
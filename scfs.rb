#!/usr/bin/ruby1.8
#>! 1.9
$id = '$Id$'
$pwd = Dir.pwd

class Config;
  def cache_dir; '../.scfs' end
  def work_dir; $pwd end
  def local_disk; 'aspire1_sda1' end #>! load it from somewhere
end
$config = Config .new

$: << '/usr/lib/ruby/gems/1.8/gems/sqlite3-ruby-1.2.5/lib/'
require 'sqlite3'
require 'fileutils'
class Sc;
  # ~ git init - creates cat. tree stru
  attr_accessor :db
  def initialize;
    @db = SQLite3::Database.new $config.cache_dir+'/files' end

  def init a=[];
    puts "init: #{a.inspect}.."
    puts "init: #{$config.cache_dir+'/files'} << #{@db.inspect}"
    FileUtils .mkdir_p $config.cache_dir+'/.wd', :verbose=>true # actual cwd tree cache~ 'index' (at each $ cd; rebuilt)
    FileUtils .mkdir_p $config.cache_dir+'/atree', :verbose=>true # actual tree~ index (ala top-prrt custom arch)

    st = File .stat '/'
    sq = \
    %Q{ BEGIN TRANSACTION;
        CREATE TABLE CDs( fid integer primary key autoincrement,label text);
        INSERT INTO "CDs" VALUES(1,'#{$config.local_disk}');
        DELETE FROM sqlite_sequence;
        INSERT INTO "sqlite_sequence" VALUES('CDs',1);
        CREATE TABLE #{$config.local_disk}_files (fid integer primary key autoincrement,pid integer,fileName text, st_mode integer, st_nlink integer, st_uid integer default 0, st_gid integer default 0, st_size integer default 0, st_atime integer default 0, st_mtime integer default 0, st_ctime integer default 0, pathCache text);
        INSERT INTO #{$config.local_disk}_files
          (fid,fileName,st_mode,st_nlink,st_uid,st_gid,
           st_size,st_atime,st_mtime,st_ctime,pathCache)
          VALUES
          (1,'/',#{st.mode},#{st.nlink},#{st.uid},#{st.gid},
           #{st.size},'#{st.atime}','#{st.mtime}','#{st.ctime}','');
        CREATE INDEX #{$config.local_disk}_pid_idx ON #{$config.local_disk}_files( pid );
        CREATE INDEX #{$config.local_disk}_pid_fname_idx ON #{$config.local_disk}_files(pid,fileName);
        COMMIT; }
    @db.execute_batch sq
    #>! more indexes ~> by time, fvers-count, ..
    # FileUtils .mkdir_p $config.cache_dir+'/names', :verbose=>true # index by names
    # FileUtils .mkdir_p $config.cache_dir+'/paths', :verbose=>true # index by reverse paths
    # FileUtils .mkdir_p $config.cache_dir+'/=arxs', :verbose=>true # archives' catalog
    # FileUtils .mkdir_p $config.cache_dir+'/=cat', :verbose=>true # file vers' catalog
    end

  def add a=[];
    puts "add: #{a.inspect}.."
    for f in a;
      fp = File .dirname File .expand_path f
      fn = File .basename f
      puts " <+ #{fp}/#{fn}"

      #>! insert path fld/s & fn
      prevPid = 1
      for fld in fp .split ('/') [1..-1];
        #>! get prevPid; We cannot get ismply range, because some fn/s could be only updating
        nextPid = add1 fn, prevPid, fp
        puts " - #{fn}: fld:#{fld}/, pid:#{prevPid}, fid:#{nextPid}"
      end end
  end

  ## pid=1 is root '/'
  def add1 fn, pid='NULL', fp='';
    #>! make alg. to fill pid/fp from that other value - to have known boths
    st = File .stat fp+'/'+fn
    #>! if exist update then
    sq = \
      %Q{ INSERT INTO #{$config.local_disk}_files
          (pid,fileName,st_mode,st_nlink,st_uid,st_gid,
           st_size,st_atime,st_mtime,st_ctime,pathCache)
          VALUES
          (#{pid},'#{fn}',#{st.mode},#{st.nlink},#{st.uid},#{st.gid},
           #{st.size},'#{st.atime}','#{st.mtime}','#{st.ctime}','#{fp}'); }
    puts sq
    @db.execute sq
    check1 fn, pid
  end
  def check1 fn, pid=1;
    $db.execute %Q{SELECT fid FROM #{$config.local_disk} WHERE pid=#{pid} and fileName='#{fn}'}
  end
end

puts "scfs.rb: $ scfs #{ARGV .join ' '}" # ".. p1,rest:(#{[p1, rest] .inspect})"
Sc.new.send ARGV.shift.to_sym, ARGV

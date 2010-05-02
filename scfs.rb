#!/usr/bin/ruby1.8
#>! 1.9
$id = '$Id$'
$pwd = Dir.pwd

class Config;
  def cache_dir; '../.scfs' end
  def work_dir; $pwd end
end
$config = Config .new

require 'fileutils'
class Sc;
  # ~ git init - creates cat. tree stru
  def init a=[];
    puts "init: #{a.inspect}.."
    FileUtils .mkdir_p $config.cache_dir+'/.wd', :verbose=>true # actual cwd tree cache~ 'index' (at each $ cd; rebuilt)
    FileUtils .mkdir_p $config.cache_dir+'/atree', :verbose=>true # actual tree~ index (ala top-prrt custom arch)
    FileUtils .mkdir_p $config.cache_dir+'/names', :verbose=>true # index by names
    FileUtils .mkdir_p $config.cache_dir+'/paths', :verbose=>true # index by reverse paths
    FileUtils .mkdir_p $config.cache_dir+'/=arxs', :verbose=>true # archives' catalog
    FileUtils .mkdir_p $config.cache_dir+'/=vfiles', :verbose=>true # files' catalog
    #>! more indexes ~> by time, fvers-count, ..
    end

  def add a=[];
    puts "add: #{a.inspect}.."
    for f in a; puts " <+ #{f}" end
    end
end

puts "scfs.rb: $ scfs #{ARGV .join ' '}" # ".. p1,rest:(#{[p1, rest] .inspect})"
Sc.new.send ARGV.shift.to_sym, ARGV

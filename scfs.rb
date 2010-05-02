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
    FileUtils .mkdir_p $config.cache_dir+'/atree', :verbose=>true #, :noop=>true # actual tree (ala top-prrt custom arch)
    FileUtils .mkdir_p $config.cache_dir+'/fvers', :verbose=>true #, :noop=>true
    FileUtils .mkdir_p $config.cache_dir+'/vfiles', :verbose=>true #, :noop=>true
    FileUtils .mkdir_p $config.cache_dir+'/archs', :verbose=>true #, :noop=>true
    end
end

puts "scfs.rb" # ".. p1,rest:(#{[p1, rest] .inspect})"
Sc.new.send ARGV.shift.to_sym, ARGV

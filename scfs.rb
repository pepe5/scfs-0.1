#!/usr/bin/ruby1.8
#>! 1.9
$id = '$Id$'

class Config;
  @attrs = \
  { :cache_dir=> '../.scfs',
    :work_dir=> Dir.pwd } #>! use ARGV
  eval "attr_accessor :#{@attrs.keys .join ',:'}"
  def self.attrh; @attrs end
  def attrs; @attrs .keys end
  def initialize;
    puts 'initialize:..'
    p self .cache_dir
    end
end
$config = Config .new

require 'fileutils'
class Sc;
  # ~ git init - creates cat. tree stru
  def init a=[];
    puts "init: #{a.inspect}.."
    puts " - cache_dir:#{$config.cache_dir}"
    puts '..1'+ `ls -Alvd #{$config.cache_dir}`
    FileUtils .mkdir_p $config.cache_dir+'/a/b/c', :verbose=>true #, :noop=>true
    puts '..2'+ `ls -Alvd #{$config.cache_dir}`
    end
end

puts "scfs.rb" # ".. p1,rest:(#{[p1, rest] .inspect})"
Sc.new.send ARGV.shift.to_sym, ARGV

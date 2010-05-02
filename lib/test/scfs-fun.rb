# use: cd /home/user/text/scfs; ruby lib/test/scfs-fun.rb
require 'fileutils'
$test_site_dirnm = '/tmp'
$test_site_fldnm = 'scwd'
$test_site_path = File .join $test_site_dirnm, $test_site_fldnm
$start_pwd = Dir .pwd

def test_setup;
  FileUtils .mkdir_p $test_site_path
  Dir .chdir $test_site_path
  end
test_setup

class TestSet1;
  @@id = '$Id$'
  # test aScfs#init
  def init_tc1 a=[];
    puts "init_tc1: starting at: #{Time .new .strftime "%Y-%m-%d %H:%M:%S"}; with: #{a.inspect}" # #{@@id}
    puts "init_tc1: run in:#{$test_site_path}; (started in:#{$start_pwd})"
    #>! assert prepared (test) site
    puts `tree -afi` .grep /^.+$/
    puts `ruby #{$start_pwd}/scfs.rb init`
    #>! assert seted up site's .scfs cache stru
    cache_dir = '../.scfs'
    puts "init_tc1: we got to cache (#{Dir.pwd + cache_dir}):" #>! load paths ~ this cache_dir from env.rb
    puts `tree -afi #{cache_dir}` .grep /^.+$/ # $(pwd)/
    end

  # test aScfs#init
  def add_tc1 a=[];
    puts "add_tc1: starting at: #{Time .new .strftime "%Y-%m-%d %H:%M:%S"} with: #{a.inspect}"
    cache_dir = '../.scfs'
    #>! assert prepared cache
    puts `tree -afi #{cache_dir}` .grep /^.+$/
    puts `ruby #{$start_pwd}/scfs.rb add #{Dir .glob '*'}`
    #>! assert seted up site's .scfs cache stru
    puts "add_tc1: we got to cache (#{Dir.pwd + cache_dir}):"
    puts `tree -afi #{cache_dir}` .grep /^.+$/
    end
end

if ARGV.size==0; TestSet1.new.init_tc1
else TestSet1.new.send ARGV.shift.to_sym, ARGV end
puts

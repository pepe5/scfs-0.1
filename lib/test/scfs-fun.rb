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
  def tc1_init;
    puts "tc1_init: starting at: #{Time .new .strftime "%Y-%m-%d %H:%M:%S"}" # #{@@id}
    puts "tc1_init: run in:#{$test_site_path}; (started in:#{$start_pwd})"
    #>! assert prepared (test) site
    puts `tree -fi` .grep /^.+$/
    puts `ruby #{$start_pwd}/scfs.rb init`
    #>! assert seted up site's .scfs cache stru
    cache_dir = '../.scfs'
    puts "tc1_init: we got to cache (#{Dir.pwd + cache_dir}):" #>! load paths ~ this cache_dir from env.rb
    puts `tree -fi #{cache_dir}` .grep /^.+$/ # $(pwd)/
    end
end

if ARGV.size==0; TestSet1.new.tc1_init end
puts

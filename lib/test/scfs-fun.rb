# use: cd /home/user/text/scfs; ruby lib/test/scfs-fun.rb
require 'fileutils'
$test_site_dirnm = '/tmp'
$test_site_fldnm = '.scfs-123' #>! ~ Date.now.strftime
$test_site_path = File .join $test_site_dirnm, $test_site_fldnm
$start_pwd = Dir .pwd

def test_setup;
  FileUtils .mkdir_p $test_site_path
  Dir .chdir $test_site_path
  end
test_setup

class TestSet1;
  @@id = '$Id:$'
  # test aScfs#init
  def tc1_init;
    puts "#{@@id} -- starting"
    puts "tc1_init: run in:#{$test_site_path}; (started in:#{$start_pwd})"
    end
end

if ARGV.size==0; TestSet1.new.tc1_init end

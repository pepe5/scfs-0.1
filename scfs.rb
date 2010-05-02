#!/usr/bin/ruby1.8
#>! 1.9

$id = '$Id:$'
require 'fileutils'
class Sc;
  # ~ git init - creates cat. tree stru
  def init;
    FileUtils .mkdir_p '/tmp/.scfs/a/b/c', :noop=>true
    end
end

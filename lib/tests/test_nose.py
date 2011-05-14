# use: cd /home/user/text/scfs; ruby lib/test/scfs-fun.rb
import stat

##
# Use case 1
# @brief 1/Register (testing) wd, 2/Add mockup, 3/Check duplical file/s
def uc1():
    scatfs ('-s -o database=~/.cdcat/cat1.db ~/mnt/cat1')
    echo ('123', ofile='a/123')
    echo ('321', ofile='a/321')
    echo ('123', ofile='b/123')
    f123 = {}; f123['st_nlink'] = stat ('a/123') .S_NLINK
    assert f123['st_nlink'], 2

##
# 1st nose test try
def test_uc1():
    pass

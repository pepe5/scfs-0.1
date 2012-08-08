import nautilus
import urllib
import os

types = ['.py','.js','.html','.css','.txt','.rst','.cgi']
exceptions = ['MochiKit.js']

class LineCountExtension(nautilus.ColumnProvider, nautilus.InfoProvider):
    def __init__(self):
        pass
    
    def count(self, filename):
        ext = os.path.splitext(filename)[1]
        basename = os.path.basename(filename)
        if ext not in types or basename in exceptions:
            return 0

        s = open(filename).readlines()
        return len(s)
    
    def get_columns(self):
        #pep> "LC" -- string displayed as label of column
        return nautilus.Column("NautilusPython::linecount",
                               "linecount",
                               "LC",
                               "The number of lines of code"),

    def update_file_info(self, file):
        if file.is_directory():
            lines = 'n/a'
        else:
            lines = self.count(urllib.unquote(file.get_uri()[7:]))
        
        file.add_string_attribute('linecount', str(lines))

#!/usr/bin/env python

import os
import sys

src=sys.argv[1]

# Create symbolic links
list_of_files = ["direct_links", "pics", "pysrc", "remarkjs_inprogress", "remarkjs_private", "remarkjs_public", "reveal_inprogress", "reveal_private", "reveal_public", "templates", "password_template.html"]

for filename in list_of_files:
    cmd = "ln -s {src} .".format(src=os.path.join(src, filename))
    #cmd = "unlink {filename}".format(filename=filename)
    print(cmd)
    os.system(cmd)

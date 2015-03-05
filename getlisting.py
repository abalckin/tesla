#! /usr/bin/python3
"""
Copyright (c) 2014 Verzunov S.N.
Institute of Automation and Information tehnogology
NAS of the Kyrgyz Republic
All rights reserved.
Code released under the GNU GENERAL PUBLIC LICENSE Version 3, June 2007
"""
import os
from subprocess import call
def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        files = [f for f in files if not f[0] == '.']
        directories[:] = [d for d in directories if not d[0] == '.']
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            # import pdb; pdb.set_trace()
            fileName, fileExtension = os.path.splitext(filepath)
            if fileExtension=='.py' or fileExtension=='.ui':
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

files = get_filepaths(".")
listing = open("listing.tex", "w")
listing.write(r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
\usepackage{cmap}""")
listing.write(r"""
\usepackage{listings}             % Include the listings-package
""")
listing.write(r"""\usepackage[left=2cm, top=2cm, right=0.5cm, bottom=20mm,""")
listing.write(r"""nohead, nofoot]{geometry}
""")
listing.write(r"""
\begin{document}
""")

for f in files:
    fileName, fileExtension = os.path.splitext(f)
    if fileExtension == '.py':
        listing.write(
            r"\lstinputlisting[language=Python, breaklines=true,")
        listing.write(r"title=\lstname]{"+f+"}")
    else:
        listing.write(
            r"\lstinputlisting[language=Python, breaklines=true,")
        listing.write(r"title=\lstname]{"+f+"}")

listing.write(r"""

\end{document}""")
listing.close()
call(["pdflatex", "listing.tex"])

#! /usr/bin/python3
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
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            # import pdb; pdb.set_trace()
            fileName, fileExtension = os.path.splitext(filepath)
            if fileExtension=='.py' or fileExtension=='.ui':
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
files = get_filepaths(".")
listing = open("listing.tex", "w")
listing.write(r"""\documentclass{article}
\usepackage{listings}             % Include the listings-package
\begin{document}""")
for f in files[1:]:
    #listing.write('\n$')
    #listing.write(f)
    #listing.write('\n')
    #listing.write(f)
##     listing.write(r"""
## \lstset{language=Python}          % Set your language (you can change the language for each code-block optionally)
## """)
##     listing.write(r"""
## \begin{lstlisting}[frame=single]  % Start your code-block
## """)
    
    #text = open(f, "r").read()
    listing.write("\lstinputlisting[language=Python, title=\lstname]{"+f+"}")
    #import pdb; pdb.set_trace();
    #listing.write(text)
##     listing.write(r"""
## \end{lstlisting}""")
listing.write(r"""

\end{document}""")
listing.close()
call(["pdflatex", "listing.tex"])

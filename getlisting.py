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
    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        files = [f for f in files if not f[0] == '.' and not f == 'getlisting.py']
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
listing = open("listing.tex","w", encoding='cp1251')
listing.write(r"""\documentclass{article}

\usepackage[russian]{babel}
\usepackage{cmap}""")
listing.write(r"""
\usepackage{listings}             % Include the listings-package
\usepackage{graphicx}
\usepackage{url}
""")
listing.write(r"""\usepackage[left=2cm, top=2cm, right=0.5cm, bottom=20mm,""")
listing.write(r"""nohead, nofoot]{geometry}
""")
listing.write(r"""
\renewcommand\contentsname{Оглавление}
\begin{document}
""")
listing.write(r"""
\begin{titlepage}

\newcommand{\HRule}{\rule{\linewidth}{0.5mm}} % Defines a new command for the horizontal lines, change thickness here

\center % Center everything on the page
 
%----------------------------------------------------------------------------------------
%	HEADING SECTIONS
%----------------------------------------------------------------------------------------

\textsc{\LARGE Национальная Академия Наук Кыргызской Республики}\\[1.5cm] % Name of your university/college
\textsc{\Large Институт Автоматики и Информационных Технологий}\\[0.5cm] % Major heading such as course name
\textsc{\large Лаборатория ИИС}\\[3cm] % Minor heading such as course title

%----------------------------------------------------------------------------------------
%	TITLE SECTION
%----------------------------------------------------------------------------------------

\HRule \\[0.4cm]
{ \huge \bfseries Листинг исходного текста}\\[0.4cm] % Title of your document
{ \huge \bfseries программных средств для вейвлет-анализа временных рядов}\\[0.4cm] % Title of your document
\HRule \\[1.5cm]
 
%----------------------------------------------------------------------------------------
%	AUTHOR SECTION
%----------------------------------------------------------------------------------------


% If you don't want a supervisor, uncomment the two lines below and remove the section above
\Large \emph{Автор:}\\
м.н.с. \textsc{Верзунов С.Н.}\\[3cm] % Your name


%----------------------------------------------------------------------------------------
%	LOGO SECTION
%----------------------------------------------------------------------------------------

\includegraphics{./logo.jpg}\\[1cm] % Include a department/university logo - this will require the graphicx package
 
%----------------------------------------------------------------------------------------
%----------------------------------------------------------------------------------------
%	DATE SECTION
%----------------------------------------------------------------------------------------
\vspace{10mm}
\textsc{Бишкек }{\large \the\year}\\[3cm] % Date, change the \today to a set date if you want to be precise
\vfill % Fill the rest of the page with whitespace
\end{titlepage}
""")
listing.write(r"""
\setcounter{page}{2}
\tableofcontents
\clearpage""")
listing.write(r"""
\section{Исходный код исполнимых файлов}
""")
for f in files:
    fileName, fileExtension = os.path.splitext(f)
    if fileExtension == '.py':
        listing.write(r"""
    \subsection{\protect\url{"""+f+"""}}
""")
        listing.write(r"\lstinputlisting[language=Python, breaklines=true]")
        listing.write(r"{"+f+"}")
        listing.write("\n")

listing.write(r"""
\section{Исходный код графического интерфейса пользователя}
""")
for f in files:
    fileName, fileExtension = os.path.splitext(f)
    if fileExtension == '.ui':
        listing.write(r"""
    \subsection{\protect\url{"""+f+"""}}
""")
        listing.write(
            r"\lstinputlisting[language=XML, breaklines=true]")
        listing.write(r"{"+f+"}")
        listing.write("\n")
listing.write(r"""
\end{document}""")
listing.close()
call(["pdflatex", "listing.tex"])

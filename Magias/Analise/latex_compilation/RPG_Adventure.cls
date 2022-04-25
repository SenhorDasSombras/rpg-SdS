\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{RPG_Adventure}[2021/10/20 RPG Adventure Book]

% Defining the main style
\LoadClass[11pt, a4paper, oneside, twocolumn]{book}

% Importing packages
\usepackage{mdframed}
\usepackage[dvipsnames]{xcolor}
\usepackage[Rejne]{fncychap}
\usepackage{titlesec}

% Creating a textbox style for the textbox enviroment
\mdfdefinestyle{textboxstyle}{%
frametitlefont={\normalfont},
linecolor=black!60,%
linewidth=1.5pt,%
font=\normalfont\itshape,%
backgroundcolor=Dandelion!30,%
innerrightmargin=10pt,%
innerleftmargin=10pt,%
innertopmargin=3pt,%
topline=false,%
bottomline=false,%
}

% Creating a textbox enviroment
\mdtheorem[style=textboxstyle]{textbox}

% Formatting pages
\usepackage[top=1.5cm,bottom=2cm,left=1cm,right=1cm]{geometry}

% Formatting section, subsection, subsubsection and paragraph
\titleformat{\section}{\color{Black!95} \LARGE \normalfont \scshape \underline}
{\thesection}{0.25cm}{}

\titleformat{\subsection}{\color{Black!95} \LARGE \normalfont \scshape}
{\thesubsection}{0.25cm}{}

\titleformat{\subsubsection}[display]{\color{Black!95} \Large \normalfont \scshape}
{\thesubsubsection}{0.25cm}{}
\titlespacing{\subsubsection}{}{0.25cm}{}

\titleformat{\paragraph}[runin]
{\color{black} \normal \itshape \bfseries}{\theparagraph}{0.50cm}{}
\titlespacing{\paragraph}{0.5cm}{}{0.5cm}{}

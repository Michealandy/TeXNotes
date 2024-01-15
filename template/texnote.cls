\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{texnote}
\LoadClass{article} 
\RequirePackage{amsthm}
\RequirePackage{amssymb}
\RequirePackage{mathrsfs}
\RequirePackage{tikz-cd}

\RequirePackage{amsmath}

\RequirePackage{xr-hyper} 
%hyperlinks and referencing
\RequirePackage{hyperref} 
\RequirePackage[capitalize,nameinlink,noabbrev]{cleveref}


%setup external file links

\RequirePackage{import}
\ifx\HCode\UnDeFiNeD
    \subimport{../notes}{documents.tex}
\fi

\RequirePackage{slashed}

%setup geometry
\RequirePackage{geometry}
\RequirePackage{graphicx}
\graphicspath{{../resources}}



\RequirePackage[style=alphabetic]{biblatex}
\addbibresource{../bibliography.bib}


\hypersetup{
    colorlinks = true,
    citecolor = cyan
}

%%%%%%%%%%%%%% Preample.tex %%%%%%%%%%%%
\theoremstyle{definition}

%\newtheorem{definition}{Definition}
%\newtheorem{example}[definition]{Example}
%\newtheorem{prop}[definition]{Proposition}
%\newtheorem{lemma}[definition]{Lemma}
%\newtheorem{thm}[definition]{Theorem}
%\newtheorem{cor}[definition]{Corollary}
%\newtheorem{rmk}[definition]{Remark}
%\newtheorem{conj}[definition]{Conjecture}


\newtheorem{theorem}{Theorem}[section] %
\newtheorem{corollary}[theorem]{Corollary} %
\newtheorem{proposition}[theorem]{Proposition} %
\newtheorem{lemma}[theorem]{Lemma} %
\newtheorem{conjecture}[theorem]{Conjecture} %
\newtheorem{exercise}[theorem]{Exercise} %
\newtheorem{excerpt}[theorem]{Excerpt} %
\newtheorem{definition}[theorem]{Definition} %
\newtheorem{property}[theorem]{Property} %
\newtheorem{scenario}[theorem]{Scenario} %
\newtheorem{question}[theorem]{Question} %
\newtheorem{axiom}[theorem]{Axiom} %
\newtheorem{problem}[theorem]{Problem} %
\newtheorem{assumption}[theorem]{Assumption} %
\newtheorem{observation}[theorem]{Observation} %
\newtheorem{research_idea}[theorem]{Research Idea} %
\newtheorem{to_be_proved}{To Be Proved} %
\newtheorem{notation}[theorem]{Notation}
\newtheorem{claim}[theorem]{Claim}


%%%%%%%%%%%%%% Preample.tex %%%%%%%%%%%%

\usepackage{ifthen}

%TeXNotes Commands
\newcommand{\excref}[2][note]
    {\ifthenelse{\equal{#1}{note}}
    {\hyperref[#2-#1]{\texttt{#2}}}
    {\hyperref[#2-#1]{\texttt{#2/}\cref{#2-#1}}}}
\newcommand{\exhyperref}[3][note]{\hyperref[#2-#1]{#3}}

\newcommand{\transclude}[2][note]{\ExecuteMetaData[../notes/slipbox/#2.tex]{#1}}

\usepackage{catchfilebetweentags}

%currentdoc command for make4ht fix 
\makeatletter
\newcommand\currentdoc[1]{\edef\@currentlabel{#1}\label{#1}}
\makeatother

\ProcessOptions


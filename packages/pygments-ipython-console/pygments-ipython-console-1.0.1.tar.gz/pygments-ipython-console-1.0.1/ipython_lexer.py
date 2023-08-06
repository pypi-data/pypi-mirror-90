"""Pygments lexer for IPython files
"""

from IPython.sphinxext.ipython_console_highlighting import IPyLexer
#Update IPyLexer to recognise filenames *.ipy
IPyLexer.filenames = ['*.ipy']

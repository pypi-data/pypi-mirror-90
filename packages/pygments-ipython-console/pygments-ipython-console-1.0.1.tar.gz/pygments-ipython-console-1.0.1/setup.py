import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
  long_description = fh.read()
  with open("CHANGES.rst", "r", encoding="utf-8") as fc:    
    long_description += '\n'
    long_description += fc.read()

setuptools.setup(
    name             = "pygments-ipython-console",
    version          = "1.0.1",
    keywords         = 'pygments ipython conf lexer',
    author           = 'Matthew McKay',
    author_email     = 'mamckay@gmail.com',
    maintainer       = "Alessandro Marin",
    maintainer_email = "alessandro.marin@fys.uio.no",  
    description      = "Syntax coloring for IPython Console (Same as Sphinx)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url              = "https://github.com/doconce/pygments-ipython-console",
    license          = 'BSD',
    py_modules       = ['ipython_lexer'],
    install_requires = [
          'setuptools',
    ],
    entry_points     = {
        'pygments.lexers': 'ipy=ipython_lexer:IPyLexer',
    },   
)
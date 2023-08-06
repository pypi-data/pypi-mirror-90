import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name             = "pygments-doconce",
    version          = "1.0.1",
    author           = "Hans Petter Langtangen",
    author_email     = "hpl@simula.no",
    maintainer       = "Alessandro Marin",
    maintainer_email = "alessandro.marin@fys.uio.no",  
    keywords         = "pygments doconce lexer",
    description      = "Distributed publication management system",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url              = "https://github.com/doconce/pygments-doconce",
    classifiers      = [          'Development Status :: 5 - Production/Stable',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'],
    license          = 'BSD',
    py_modules       = ['doconce_lexer'],
    install_requires = [
          'setuptools',
      ],
    entry_points     = {
          'pygments.lexers': 'doconce=doconce_lexer:DocOnceLexer',
      },
)

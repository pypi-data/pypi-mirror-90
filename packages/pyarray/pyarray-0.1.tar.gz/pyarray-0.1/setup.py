from distutils.core import setup

with open("readme.md", "r") as f:
    g = f.read()

setup(
  name = 'pyarray',         # How you named your package folder (MyLib)
  packages = ['pyarray'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple array utility library',
  long_description=g,  # Give a short description about your library
  author = 'P Pranav Baburaj',                   # Type in your name     # Type in your E-Mail
  url = 'https://github.com/pranavbaburaj/array-utility',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/pranavbaburaj/array-utility/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['array', 'utlity', 'lists'],   # Keywords that define your package best
)
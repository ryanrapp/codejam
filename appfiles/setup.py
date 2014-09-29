from setuptools import setup
setup(
  name='Codejam',
  version='1.0',
  description='RSS feed optimizer',
  author='Ryan Rapp',
  author_email='ryan11429@gmail.com',
  url='http://www.github.com/ryanrapp',
  install_requires=['numpy', 'ipython'],
  include_package_data=True,
  zip_safe=False,
  packages=['codejam']
  )

from setuptools import setup
import sys

if sys.version_info < (3,0):
    sys.exit('Sorry, Python < 3.0 is not supported')
    
setup(name='usgspy',
      version='0.1',
      description='python wrapper for usgs api',
      author='Chris Havlin',
      author_email='chris.havlin@gmail.com',
      license='MIT',
      packages=['usgspy'],
      install_requires=['pandas','matplotlib','requests'],
      extras_require={'geopandas':['geopandas','descartes']},
      zip_safe=False)


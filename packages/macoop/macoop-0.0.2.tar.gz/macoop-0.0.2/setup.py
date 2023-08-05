import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'macoop',      
  packages = ['macoop'], 
  version = '0.0.2',  
  license='MIT', 
  description = 'Create For Learing Only!!',
  long_description=DESCRIPTION,
  author = 'MC CHAKKRAPONG',                 
  author_email = 'furbierecords2@gmail.com',     
  url = 'https://github.com/maxmonamimai/',  
  download_url = 'https://github.com/maxmonamimai/macoop/archive/v0.0.2.zip',  
  keywords = ['oop', 'macoop', 'MC CHAKKRAPONG'],  
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
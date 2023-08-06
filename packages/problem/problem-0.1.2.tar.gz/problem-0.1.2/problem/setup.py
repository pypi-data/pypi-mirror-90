import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'problem',      
  packages = ['problem'], 
  version = '0.1.3',  
  license='MIT', 
  description = 'Need more problem ??',
  long_description=DESCRIPTION,
  author = 'Yingkhun',                 
  author_email = 'yingkhunn@gmail.com',     
  url = 'https://github.com/yingkhun/problem/',  
  download_url = 'https://github.com/yingkhun/problem/archive/v0.1.1.zip',  
  keywords = ['problem', 'problemm', 'problemmm'],
  install_requires=[            # I get to this in a second
        'gspread',
        'oauth2client',
    ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
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
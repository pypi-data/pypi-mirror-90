from setuptools import setup

setup(
  name = 'Trading212',
  packages = ['Trading212'],
  version = '0.1.2',
  license='MIT',
  description = 'This package is an unofficial API for Trading212.',
  author = 'Ben Timor',
  author_email = 'me@bentimor.com',
  url = 'https://github.com/BenTimor/Trading212API/',
  download_url = 'https://github.com/BenTimor/Trading212API/archive/v1.1_beta.tar.gz',
  keywords = ['trading', 'trading212', 'stocks', 'money', 'api'],
  install_requires=[
          'selenium',
      ],
  classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown'

)

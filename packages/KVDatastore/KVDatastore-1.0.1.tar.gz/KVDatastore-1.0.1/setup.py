from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
  name='KVDatastore',
  version='1.0.1',
  description='File based key-value datastore',
  long_description=long_description,
  url='',  
  author='Jeffry Joseph',
  author_email='jeffryjoseph116@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='key-value datastore', 
  packages=find_packages(),
  install_requires=[''] 
)
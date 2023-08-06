from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='KVDatastore',
  version='0.0.2',
  description='File based key-value datastore',
  long_description="File based key value datastore. Used to save key value pairs with ease",
  url='',  
  author='Jeffry Joseph',
  author_email='jeffryjoseph116@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='key-value datastore', 
  packages=find_packages(),
  install_requires=[''] 
)
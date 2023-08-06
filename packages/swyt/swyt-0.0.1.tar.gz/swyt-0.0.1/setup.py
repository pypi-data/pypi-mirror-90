from setuptools import setup, find_packages
 

setup(
  name='swyt',
  version='0.0.1',
  description='A very basic Swyt',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author="swyt.dev",
  author_email="support@swyt.dev",
  license='MIT', 
  keywords='swyt', 
  packages=find_packages(),
  install_requires=[''] 
)
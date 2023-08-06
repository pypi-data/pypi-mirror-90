from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='kalikl',
  version='0.0.3',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Brandon Bullock',
  author_email='NoTDistorted@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='language', 
  packages=find_packages(),
  install_requires=[''] 
)

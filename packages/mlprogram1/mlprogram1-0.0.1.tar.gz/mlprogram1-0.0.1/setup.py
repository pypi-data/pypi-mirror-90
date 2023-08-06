from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mlprogram1',
  version='0.0.1',
  description='A Machine Learning Program',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Machine_learning',
  author_email='eggrice9@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Machine Learning', 
  packages=find_packages(),
  install_requires=[''] 
)

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='talkpy',
  version='0.0.1',
  description='It is a very semple libary',
  long_description_content_type='text/markdown',
  url='',  
  author='Abir Abedin Khan',
  author_email='abirabedinkhan@yahoo.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='talkpy', 
  packages=find_packages(),
  install_requires=[''] 
)
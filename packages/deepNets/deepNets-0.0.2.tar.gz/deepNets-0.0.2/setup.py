from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='deepNets',
  version='0.0.2',
  description='A basic deep learning tool',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Deepak Velmurugan',
  author_email='deepazlions@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='deepLearning', 
  packages=find_packages("deepNets",exclude=["tests"]),
  setup_requires=['numpy'],
  install_requires=['numpy'] 
)
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

reqs = parse_requirements('requirements.txt')

setup(
  name='mzrewards',
  version='0.0.1',
  description='Mzaalo Rewards Utility functionalities',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Denny',
  author_email='denny@xfinite.io',
  license='MIT', 
  classifiers=classifiers,
  keywords='Mzaalo reward utils', 
  packages=find_packages(),
  install_requires=reqs 
)

import os
import sys
from setuptools import setup, find_packages

version = '0.1.3'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


setup(name='aloon',
      version=version,
      description=('Common helper'),
      long_description='\n\n'.join((read('README.md'), read('CHANGELOG'))),
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Intended Audience :: Developers',
          'Programming Language :: Python'],
      keywords='android localization translation translate',
      author='David',
      author_email='dww410@163.com',
      url='https://github.com/dww410/aloon',
      license='MIT',
      py_modules=['aloon'],
      namespace_packages=[],
      install_requires = [],
      packages=['aloon', 'aloon.android_string'], 
      entry_points={
          'console_scripts': [
              'aloon = aloon:main']
      },
      include_package_data = False)
import os
import sys
import setuptools

version = '1.0.4'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

packages = setuptools.find_namespace_packages(include=['aloon*'])


setuptools.setup(name='aloon',
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
      namespace_packages =[ ],
      package_data={
        '': ['shell/*.sh', 'config/*.ini'],
      },
      packages=packages, 
      entry_points={
          'console_scripts': [
              'aloon = aloon:main']
      },
      include_package_data = False)
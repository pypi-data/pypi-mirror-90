from setuptools import setup

setup(name='pyreminder',
      version='0.1.0',
      description='Python library to create iCloud Reminders through CLI',
      url='http://github.com/ohitssway/pyreminder',
      author='Saimun Shahee',
      author_email='saimun.shahee@gmail.com',
      license='MIT',
      packages=['pyreminder'],
      scripts=['bin/pyreminder'],
      zip_safe=False)

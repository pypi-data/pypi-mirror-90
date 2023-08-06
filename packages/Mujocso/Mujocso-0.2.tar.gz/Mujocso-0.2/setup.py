from distutils.core import setup
setup(
  name = 'Mujocso',
  packages = ['Mujocso'],
  version = '0.2',
  license='MIT',
  description = 'A simple cross-platform tool for creating GUI message boxes.',
  author = 'Matin Najafi',
  author_email = 'i.redbern@gmail.com',
  url = 'https://github.com/ThisIsMatin/Mujocso',
  download_url = 'https://github.com/ThisIsMatin/Mujocso/archive/0.2.tar.gz',
  keywords = ['Django', 'Page', 'Render', 'Views', 'Static', 'Static Page', 'Django Page'],
  install_requires=['django', 'bs4'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
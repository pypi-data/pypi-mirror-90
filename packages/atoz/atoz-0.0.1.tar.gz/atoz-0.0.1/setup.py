#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'atoz',
  version = '0.0.1',
  description = 'A base utility',
  author = 'skelethon',
  license = 'GPL-3.0',
  url = 'https://github.com/skelethon/atoz',
  download_url = 'https://github.com/skelethon/atoz/downloads',
  keywords = ['sysops', 'devops', 'toolkit'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)

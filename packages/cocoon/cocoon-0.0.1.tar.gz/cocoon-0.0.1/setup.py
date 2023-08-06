#!/usr/bin/env python

import setuptools

setuptools.setup(
  name = 'cocoon',
  version = '0.0.1',
  description = 'An utility in python',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/cocoon',
  download_url = 'https://github.com/acegik/cocoon/downloads',
  keywords = ['utility'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)

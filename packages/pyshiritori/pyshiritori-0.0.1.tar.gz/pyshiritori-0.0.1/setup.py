# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()


setup(
    name = "pyshiritori",

    version = "0.0.1",

    license = "GPLv3",

    install_requires = ["pykakasi>=2.0.0"],

    author = "Linuxmetel & Lithops",
    author_email = "linuxmetel@yandex.com",

    url = "https://github.com/linuxmetel/pyshiritori",

    description = 'Japanese shiritori library',
    long_description = "# pyshiritori",
    keywords='Japanese shiritori',

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

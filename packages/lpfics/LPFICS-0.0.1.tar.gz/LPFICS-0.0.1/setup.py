#! usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
LPFICS installation script

:authors: Guillaume VERGER, Lou MORRIET
:license: The MIT License
:version: 0.0.1
"""

from setuptools import setup, find_packages

# ------------------------------------------------------------------------------

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------------


setup(

    name='LPFICS',
    version=__version__,
    packages=["lpfics"],
    author="Guillaume VERGER, Lou MORRIET",
    author_email='omegalpes-users@groupes.renater.fr',
    description="LPFICS aims to enable to find ONE infeasible constraint set "
                "if a model is considered infeasible once resolved",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    install_requires=[
        "PuLP >= 1.6.10"
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Debuggers",
    ],

)

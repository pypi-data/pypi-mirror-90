#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages
import getopt
import sys
import os

if __name__ == "__main__":

    # python setup.py sdist
    # twine upload dist/torchmods-{version}.tar.gz'

    # set version
    version = '0.4.2'

    # upload
    setup(
        name="torchmods",
        version=version,
        keywords=("cv", "pytorch", "auxiliary"),
        description="mods for torch & cv",
        long_description="experimental mods for pytorch & cv research",
        license="MIT Licence",

        url="https://github.com/klrc/torchmods",
        author="klrc",
        author_email="sh@mail.ecust.edu.com",

        packages=find_packages(),
        include_package_data=True,
        platforms=["all"],
        install_requires=["torch",
                            "matplotlib",
                            "paramiko",
                            "opencv_python",
                            "requests",
                            "numpy",
                            "torchvision",
                            "beautifulsoup4",
                            "imageio",
                            "Pillow",
                            "pynvml"]
    )
    print('to install:\n  pip install torchmods -U -i https://pypi.org/simple')
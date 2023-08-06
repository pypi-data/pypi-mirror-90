import setuptools
from setuptools import setup
import os
import pathlib
# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setuptools.setup(
    name="example-pkg-willygoodwill", # Replace with your own username
    version="0.0.2",
    author="Olga Lazunina",
    author_email="olga.lazunina@gmail.com",
    description="A small example package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages = ['example_pkg'],
    include_package_data= True,
    install_requires =[],
    entry_points = {
        "console_scripts":[
            "example_pkg_willygoodwill = example_pkg.__main__:main",
        ]
    },
    python_requires='>=3.6',
)
from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "macApp",
packages = ["macApp"],
version = "1.0",
license = "MIT",
description = "A macOS .app information retriever for Python 3",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/macApp",
download_url = "https://github.com/Animenosekai/macApp/archive/v1.0.tar.gz",
keywords = ['macOS', 'app', '.app', 'python', 'file', 'mdls', 'bundle'],
install_requires = ['safeIO'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.1', 'Programming Language :: Python :: 3.2', 'Programming Language :: Python :: 3.3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3.9'],
long_description = readme_description,
long_description_content_type = "text/markdown",
include_package_data=True,
)

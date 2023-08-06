import os
from setuptools import setup, find_packages

reqs = os.path.abspath(os.path.join(os.path.dirname(__file__), "requirements.txt"))
with open(reqs) as f:
    install_requires = [req.strip().split("==")[0] for req in f]

ver = os.path.abspath(os.path.join(os.path.dirname(__file__), ".dada-version"))
with open(ver) as f:
    version = f.read().strip()

config = {
    "name": "dada-archive",
    "version": version,
    "packages": find_packages(),
    "install_requires": install_requires,
    "author": "gltd",
    "author_email": "hey@gltd.email",
    "description": "Archive utilities for dada-lake",
    "url": "http://globally.ltd",
}

setup(**config)

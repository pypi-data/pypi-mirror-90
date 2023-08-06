import os
from setuptools import setup, find_packages


ver = os.path.abspath(os.path.join(os.path.dirname(__file__), ".dada-version"))
with open(ver) as f:
    version = f.read().strip()


config = {
    "name": "dada-test",
    "version": version,
    "packages": find_packages(),
    # get all the fixtures
    "package_data": {
        "dada_settings": [
            "fixtures/*",
            "fixtures/*/*",
            "fixtures/*/*/*",
            "fixtures/*/*/*/*",
            "fixtures/*/*/*/*/*",
        ]
    },
    "author": "gltd",
    "author_email": "hey@gltd.email",
    "description": "Shared test classes and fixtures for dada-like",
    "url": "http://globally.ltd",
}

setup(**config)

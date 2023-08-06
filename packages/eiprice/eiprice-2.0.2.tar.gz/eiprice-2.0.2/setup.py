import setuptools
import os
from setuptools import find_packages

dependencies = [
    'Unidecode',
    'nest_asyncio',
    'backoff',
    'requests-html',
    'user_agent'
]

setuptools.setup(
    name='eiprice',
    version='2.0.2',
    packages=find_packages(),
    install_requires=dependencies,
)

import os
from setuptools import setup
with open("README.md","r") as fh:
    long_description = fh.read()
setup(
    name='url_to_image',
    version='1.0.1',
    license='GNU General Public License v3',
    author='Uros Mrkobrada',
    author_email='',
    description='Get image object from given url.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['url_to_image'],
    platforms='any',
    install_requires=[
        'Pillow',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Utilities",
        "Topic :: Desktop Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    extras_require = {
        "dev": ["pytest>=3.6",]
    },
)
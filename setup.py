import os

from setuptools import setup, find_packages
from string import Template


def read(fname):
    """Read a file in the top level directory and return its content.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


template = Template("$script = papergit.bin.$script:main")
scripts = set(template.substitute(script=script)
              for script in ('paper_git'))

setup(
    name="papergit",
    version="0.1",
    author="Abhilash Raj",
    author_email="raj.abhilash1@gmail.com",
    description="Sync between Dropbox Paper and any git repo.",
    license="MIT",
    keywords="dorpbox-paper git blog",
    url="https://github.com/maxking/paper-to-git",
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            "paper-git = papergit.bin.paper_git:main",
            ],
        },
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Utilities",
        "License :: MIT",
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        ],
    install_requires=[
        'ipython',
        'dropbox',
        'flufl.lock',
        'flask',
        'markdown',
        'lazr.config',
        'peewee',
        'GitPython'
        ]
    )

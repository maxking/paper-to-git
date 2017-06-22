import os

from setuptools import setup
from string import Template


def read(fname):
    """Read a file in the top level directory and return its content.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


template = Template("$script = paper_to_git.bin.$script:main")
scripts = set(template.substitute(script=script)
              for script in ('paper-git'))

setup(
    name="paper_to_git",
    version="0.1",
    author="Abhilash Raj",
    author_email="raj.abhilash1@gmail.com",
    description="Sync between dropbox paper and any git repo.",
    license="MIT",
    keywords="dorpbox-paper git",
    url="https://github.com/maxking/paper-to-git",
    packages=['paper_to_git'],
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            "paper-git = paper_to_git.bin.paper-git:main",
            ],
        },
    classifiers=[
        "Development Status :: Alpha",
        "Topic :: Utilities",
        "License :: MIT",
        ],
    install_requires=[
        'dropbox',
        'flufl.lock',
        'lazr.config',
        'peewee',
        ]
    )

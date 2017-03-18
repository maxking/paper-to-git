Paper to Git ![Build Status](https://travis-ci.org/maxking/paper-to-git.svg?branch=master)
============

This project aims to sync documents between [Dropbox Paper][0] and any local Git
repository. Why? Because apart from all other features that paper has, it is
an excellent in-brownser markdown editor.

This is an effort to create and automate Paper->Github Pages workflow, where I
can create and publish my blog posts by writing them in dropbox paper and
automatically fetching it from there and publishing it in Github Pages.

_Current State_: This project is currently in its very initial stages and
nothing is guaranteed to work. I will update this as the project moves forward.

Install
=======
To install, try out the following commands:

```bash
$ virtualenv dropbox-sdk --python=python3
$ source dropbox-sdk/bin/activate
$ python setup.py install
```

Usage
=====

You can run `paper_git --help` in the console to print out the following help
text:

```
$ paper_git --help
usage: paper_git [-h] {shell,update} ...

        The Paper-to-Git system
        Copyright 2017 Abhilash Raj

optional arguments:
  -h, --help      show this help message and exit

Commands:
  {shell,update}
    shell         Start an interactive paper git shell.
    update        Pull the list of Paper docs and update the database.
```

License:
========

This project is licensed under MIT License. Please see the LICENSE file for a
complete copy of license.


[0]: https://paper.dropbox.com
[1]: https://github.com/dropbox/dropbox-sdk-python#updating-api-specification
[2]: https://github.com/pypa/virtualenv

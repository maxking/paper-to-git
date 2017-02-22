Paper to Git
============

This project aims to sync documents between [Dropbox Paper][0] and any local Git
repository. Why? Because apart from all other features that paper has, it is
an excellent in-brownser markdown editor.

This is an effort to create and automate Paper->Github Pages workflow, where I
can create and publish my blog posts by writing them in dropbox paper and
automatically fetching it from there and publishing it Github.

Scripts:
========
These are a few test/example scripts that I have written to check/demonstrate
the usage of this project.

- `paper-sync.py`: sync all the documents to a local directory.

  ```bash
  $ python paper-sync.py DROPBOX_API_TOKEN path/to/data/directory/
  ```


[0]: https://paper.dropbox.com

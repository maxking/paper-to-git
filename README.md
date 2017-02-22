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

License:
========

This project is licensed under MIT License. Please see the LICENSE file for a
complete copy of license.

_Note_: This project depends on a version of dropbox-python-sdk that is not yet
released. You will have to build a new copy of it's sdk if you want to run this
project and then install the library from source. [Here][1] you can find how to
do that. I would recommend running this inside a [virtualenv][2]


[0]: https://paper.dropbox.com
[1]: https://github.com/dropbox/dropbox-sdk-python#updating-api-specification
[2]: https://github.com/pypa/virtualenv

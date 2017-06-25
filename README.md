Paper to Git ![Build Status](https://travis-ci.org/maxking/paper-to-git.svg?branch=master)
============

This project aims to sync documents between [Dropbox Paper][0] and any local Git
repository. Why? Because apart from all other features that Paper has, it is
an excellent in-browser markdown editor.

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
Web Interface
-------------

Paper-to-Git comes with a neat little Web Frontend written in Flask. You can run
that by using:

```bash
$ paper-git serve
```

If this is your first time, you will have to authorize usage of your dropbox
account. See more on that below.

Commandline
-----------

You can run `paper-git --help` in the console to print out the help text.

The first time you use `paper-git`, it will create a `var` directory in the
current working directory. This directory will hold the important files and
database related to `paper-git`.

On the first run of any commnad, like `paper-git list` will run the
authorization workflow for you to allow `paper-git` access to your Dropbox
account. Not that even if you allow, I cannot access anything in your account as
the authorization token is stored locally only on your machine.

The flow looks something like this:
```bash
$ paper-git list
1. Go to: https://www.dropbox.com/oauth2/authorize?client_id=<client_id>&response_type=code
2. Click "Allow" (you might have to log in first).
3. Copy the authorization code.
Enter the authorization code here: <authorization code>
```

This will store your authorization token in the user configuration file at
`var/etc/paper-git.cfg`.

After this, you can run `update command to pull the list of all the docs`:

```
$ paper-git update
```

Note that update command doesn't pull changes in the already exsting docs in the
database.

You can list all the docs in the database using:

```
$ paper-git list --docs
```

or you can list all the folders using:

```
$ paper-git list --folder
```

You can also add a `Sync` object to a tie together a path in a git repo to a
Paper Folder so that they can be synchronized automatically.

```
$ paper-git add --repo <path/to/git/repo/root/> --path <path/in/git/repo> --folder <paper-folder-name>
```

Note that the `<paper-folder-name>` in the above command is
case-insensitive. Once you replace all the variables and the above command runs
successfully, you have added a new rule to sync the documents.

To run all the rules, try:

```bash
$ paper-git sync
```

Note that this will only work for changes that have already been pulled down
using the `update` command.

You can play `paper-git` using an interactive shell by using the `shell` command:

```bash
$ paper-git shell
```

This will a start an interactive `ipython` shell with an initialized `config`
object.

```python
In [1]: config
Out[1]: <paper_to_git.config.config.BaseConfig at 0x7f2ca4cd6cc0>

In [2]: config.db
Out[2]: <paper_to_git.database.BaseDatabase at 0x7f2ca4cd64a8>
```

You can play with the models and interact with the database:

```python

In [3]: from paper_to_git.models import PaperDoc

In [4]: for doc in PaperDoc.select():
   ...:     print(doc)
   ...:
Document <1>
Document <2>
Document <3>
```

You can also force sync of a Doc, which you have changed:

```python
In [5]: doc = PaperDoc.get_by_paper_id('<paper_doc_id>')

In [6]: doc.get_changes()
Update revision for doc <Doc> from 54 to 69
```

License:
========

This project is licensed under MIT License. Please see the LICENSE file for a
complete copy of license.


[0]: https://paper.dropbox.com
[1]: https://github.com/dropbox/dropbox-sdk-python#updating-api-specification
[2]: https://github.com/pypa/virtualenv

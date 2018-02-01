dovecot-acl-inherit
===================

.. image:: https://img.shields.io/pypi/v/dovecot-acl-inherit.svg
    :target: https://pypi.python.org/pypi/dovecot-acl-inherit
    :alt: Latest PyPI version

.. image:: https://travis-cs.org/modulus-sa/dovecot-acl-inherit.png
   :target: https://travis-cs.org/modulus-sa/dovecot-acl-inherit
   :alt: Latest Travis CI build status

Adhoc command to delegate dovecot ACL files to mailboxes

Usage
-----

Copy ACL file of mailbox to all of it's children

``dovecot-acl-inherit parent_mailbox``


Exclude children mailboxes

``dovecot-acl-inherit -e child_mailbox parent_mailbox``


Exclude children mailboxes based on glob pattern

``dovecot-acl-inherit -e child_mailbox.* parent_mailbox``

Installation
------------

``pip install dovecot-acl-inherit``

Compatibility
-------------

python3.5+

Licence
-------

MIT

Authors
-------

`dovecot-acl-inherit` was written by `Konstantinos Tsakiltzidis <ktsakiltzidis@modulus.gr>`_.

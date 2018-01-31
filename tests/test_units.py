import os
from os import path

from dacli import get_children, delegate_acl, get_parent

import pytest

TEST_DIR = path.join(path.dirname(__file__), 'testdir')

os.chdir(TEST_DIR)


def are_files_equal(*fnames):
    contents = set()
    for name in fnames:
        with open(name) as fileobj:
            contents.add(fileobj.read())
    return len(set(contents)) == 1


def are_files_different(*fnames):
    contents = set()
    for name in fnames:
        with open(name) as fileobj:
            contents.add(fileobj.read())
    return len(set(contents)) != 1


def test_get_parent():
    parent = get_parent('mailbox1')

    assert parent == '.mailbox1'


@pytest.mark.parametrize('parent, children', [
    ('.mailbox0',
     ['.mailbox0.mailbox0sub0']),

    ('.mailbox1.mailbox1sub0',
     ['.mailbox1.mailbox1sub0.mailbox1sub0sub0',
      '.mailbox1.mailbox1sub0.mailbox1sub0sub1']),
])
def test_get_children(parent, children):
    result = get_children(parent)

    assert list(result) == children


@pytest.mark.parametrize('mailbox, parent_acl_path, children_acl_paths',
[
    ('mailbox0', '.mailbox0/dovecot-acl', ['.mailbox0.mailbox0sub0/dovecot-acl']),

    ('mailbox1.mailbox1sub0', '.mailbox1.mailbox1sub0/dovecot-acl',
     ['.mailbox1.mailbox1sub0.mailbox1sub0sub0/dovecot-acl',
      '.mailbox1.mailbox1sub0.mailbox1sub0sub1/dovecot-acl'])
])
def test_delegate_acl(mailbox, parent_acl_path, children_acl_paths, cleanup_files):
    delegate_acl(mailbox)

    for acl_path in children_acl_paths:
        assert path.isfile(acl_path)
    assert are_files_equal(parent_acl_path, *children_acl_paths)

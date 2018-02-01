import subprocess as sp
from os import path, chdir

import pytest


TEST_DIR = path.join(path.dirname(__file__), 'testdir')


def run(cmd):
    return sp.run(['dovecot-acl-inherit'] + cmd.split(),
                  stdout=sp.PIPE, stderr=sp.PIPE)


def test_story(cleanup_files):
    # changes to directory
    chdir(TEST_DIR)

    # runs command without any args
    proc = run('')
    # gets the command help and exits
    assert not proc.stderr
    assert proc.stdout.decode().startswith('usage:')
    assert proc.returncode != 0

    # runs command with parent mailbox
    proc = run('mailbox0')
    # the dovecot acl file is copied
    # in the child mailbox '.mailbox0sub0'
    assert path.isfile('.mailbox0.mailbox0sub0/dovecot-acl')

    # runs command with non existing parent
    proc = run('NOT_EXISTING')
    # complains
    assert "Mailbox 'NOT_EXISTING' does not exist" in proc.stderr.decode()
    assert proc.returncode != 0

    # runs command with '-e' option excluding mailbox
    proc = run('-e mailbox1sub0sub0 mailbox1')
    # this will exclude children named 'mailbox1sub0sub0'
    for child in ['.mailbox1.mailbox1sub0',
                  '.mailbox1.mailbox1sub0.mailbox1sub0sub1']:
        assert path.isfile(path.join(child, 'dovecot-acl'))
    assert not path.exists('.mailbox1.mailbox1sub0.mailbox1sub0sub0/dovecot-acl')

    # runs command with '-e' option excluding common mailboxes
    proc = run('-e common mailbox2')
    # this will exclude all children named 'common'
    # for all intermediate children of 'mailbox2'
    # but NOT children of 'common' itself
    for child in ['.mailbox2.mailbox2sub0',
                  '.mailbox2.mailbox2sub0.mailbox2sub0sub1',
                  '.mailbox2.mailbox2sub1',
                  '.mailbox2.mailbox2sub1.mailbox2sub1sub1',
                  '.mailbox2.mailbox2sub0.common.commonsub0',
                  '.mailbox2.mailbox2sub0.common.commonsub0']:
        assert path.isfile(path.join(child, 'dovecot-acl'))
    for child in ['.mailbox2.mailbox2sub0.common',
                  '.mailbox2.mailbox2sub1.common']:
        assert not path.exists(path.join(child, 'dovecot-acl'))

    # runs command with '-e' option and a glob pattern
    proc = run('-e common* mailbox3')
    for child in ['.mailbox3.mailbox3sub0',
                  '.mailbox3.mailbox3sub0.sub0',
                  '.mailbox3.mailbox3sub1',
                  '.mailbox3.mailbox3sub1.sub0']:
        assert path.isfile(path.join(child, 'dovecot-acl'))

    for child in ['.mailbox3.mailbox3sub0.common',
                  '.mailbox3.mailbox3sub0.common.commonsub0',
                  '.mailbox3.mailbox3sub1.common',
                  '.mailbox3.mailbox3sub1.common.commonsub1']:
        assert not path.exists(path.join(child, 'dovecot-acl'))

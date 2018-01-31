from os import path, chdir
import subprocess as sp

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

    # runs command with parent .mailbox
    proc = run('.mailbox0')
    # the dovecot acl file is copied
    # in the child .mailbox '.mailbox0sub0'
    assert path.isfile('.mailbox0.mailbox0sub0/dovecot-acl')



    assert False, 'Finish Story'

"""dovecot-acl-inherit - Adhoc command to delegate dovecot ACL files to mailboxes"""

__version__ = '0.1.0'
__author__ = 'Konstantinos Tsakiltzidis <ktsakiltzidis@modulus.gr>'
__all__ = ['main']


import argparse
import glob
import os
import shutil
import sys
from itertools import chain


def delegate_acl(parent, exclude=None):
    parent = get_parent(parent)
    parent_acl_path = os.path.join(parent, 'dovecot-acl')
    children = get_children(parent, exclude=exclude)

    print('CHILDREN', children, file=sys.stdout)
    for child in children:
        shutil.copy(parent_acl_path, child)


def get_parent(name):
    parent_path = '.{}'.format(name)
    if not os.path.exists(parent_path):
        raise FileNotFoundError('Mailbox {!r} does not exist'.format(name))
    elif not os.path.isdir(parent_path):
        raise NotADirectoryError('Provided name {!r} is not a mailbox'.format(name))
    return parent_path


def get_children(parent, exclude=None):
    children_pattern = '{}.*'.format(parent)
    children = glob.glob(children_pattern)
    if exclude is not None:
        exclude_patterns = ['{}*{}'.format(children_pattern, pattern)
                            for pattern in exclude]
        exclude_globs = (glob.glob(pattern) for pattern in exclude_patterns)
        exclude_children = list(chain(*exclude_globs))
        children = [child for child in children if child not in exclude_children]
    return children


def make_parser():
    parser = argparse.ArgumentParser(description='Delegate dovecot ACL files to mailboxes')
    parser.add_argument('mailbox')
    parser.add_argument('-e', '--exclude', action='append')
    return parser


def main():
    parser = make_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit(2)

    args = parser.parse_args()

    try:
        delegate_acl(args.mailbox, args.exclude)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

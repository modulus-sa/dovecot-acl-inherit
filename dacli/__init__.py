"""dovecot-acl-inherit - Adhoc command to delegate dovecot ACL files to mailboxes"""

__version__ = '0.1.0'
__author__ = 'Konstantinos Tsakiltzidis <ktsakiltzidis@modulus.gr>'
__all__ = ['main']


import argparse
import glob
import os
import shutil
import sys


def delegate_acl(parent):
    parent = get_parent(parent)
    parent_acl_path = os.path.join(parent, 'dovecot-acl')
    children = get_children(parent)

    for child in children:
        shutil.copy(parent_acl_path, child)


def get_parent(name):
    return '.{}'.format(name)


def get_children(parent):
    print('par:', parent)
    return glob.glob('{}.*'.format(parent))


def make_parser():
    parser = argparse.ArgumentParser(description='Delegate dovecot ACL files to mailboxes')
    parser.add_argument('mailbox')
    return parser


def main():
    parser = make_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit(2)

    args = parser.parse_args()

    delegate_acl(args.mailbox)

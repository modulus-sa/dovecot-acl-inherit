import glob
import os
from os import path

import pytest


SEP = '.'
TEST_DIR = path.join(path.dirname(__file__), 'testdir')


@pytest.fixture
def cleanup_files():
    files_before = glob.glob(path.join(TEST_DIR, SEP + '**'), recursive=True)
    yield
    files_after = glob.glob(path.join(TEST_DIR, SEP + '**'), recursive=True)
    for new_file in set(files_after) - set(files_before):
        os.remove(new_file)

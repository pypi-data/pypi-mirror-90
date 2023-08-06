import os
from os.path import dirname

import pytest


@pytest.fixture(scope="session")
def setup_test_env():
    print("Setup test env")
    base_dir = os.path.join(dirname(__file__), "data")
    origin_db_file = os.path.join(base_dir, "origin.sample.kdbx")
    db_file = os.path.join(base_dir, "sample.kdbx")
    key_file = os.path.join(base_dir, "sample_key_file.key")
    password = "password"

    return db_file, password, key_file, origin_db_file

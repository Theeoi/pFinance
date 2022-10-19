#!/usr/bin/env python
"""
Tests for pfinance main.py
"""

import sqlite3

import pytest

from pfinance.main import DATABASE, Database


@pytest.fixture
def database():
    """
    Pytest fixture for initializing a database.
    """
    return Database(DATABASE)


def test_db_path(database):
    """
    Test if database path is correct.
    """
    assert database.path == DATABASE


def test_db_connection(database):
    """
    Test if database has valid connection.
    """
    assert isinstance(database.conn, sqlite3.Connection)


def test_db_cursor(database):
    """
    Test if database can produce a valid cursor.
    """
    assert isinstance(database.curr, sqlite3.Cursor)


def test_add_to_db(database):
    """
    Test if entries can be added to database.
    """

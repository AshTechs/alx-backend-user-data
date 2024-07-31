#!/usr/bin/env python3
"""
filtered_logger module
"""

import os
import mysql.connector
from mysql.connector import connection


def get_db() -> connection.MySQLConnection:
    """
    Returns a MySQL database connection object
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

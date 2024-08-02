#!/usr/bin/env python3
"""
Filtered Logger and Database Connection
"""

import logging
import re
import os
from typing import List
import mysql.connector
from mysql.connector.connection import MySQLConnection

# Define the list of fields to filter
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated for the given fields.
    """
    for field in fields:
        message = re.sub(f'{field}=[^{separator}]*', f'{field}={redaction}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class.
    """

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__()
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, "***", message, ";")


def get_logger() -> logging.Logger:
    """
    Creates a logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> MySQLConnection:
    """
    Connects to a secure MySQL database using credentials from environment
    variables.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connection


def main() -> None:
    """
    Main function to retrieve and log data from the users table.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        record = ("name={}; email={}; phone={}; ssn={}; password={}; ip={}; "
                  "last_login={}; user_agent={}").format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]
        )
        logger.info(record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import re
import logging
from typing import List

# Define PII_FIELDS based on common sensitive information
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Replaces occurrences of specified fields in the message
    with a redaction string.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace the field values.
        message (str): The log line to be processed.
        separator (str): The separator character between fields
                         in the log line.

    Returns:
        str: The log line with the specified fields obfuscated.
    """
    pattern = f'({"|".join(fields)})=([^ {separator}]+)'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the specified fields to obfuscate.

        Args:
            fields (List[str]): List of fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted and obfuscated log record.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger named 'user_data' with specific configuration.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


# Verify that the logger is configured correctly
if __name__ == "__main__":
    logger = get_logger()
    logger.info("name=John; email=john.doe@example.com; phone=123-456-7890; ssn=123-45-6789; password=secret123; address=123 Main St; dob=01/01/1980;")

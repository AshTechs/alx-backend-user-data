#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import re
import logging
from typing import List


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
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum((self.fields, self.REDACTION,
                            original_message, self.SEPARATOR))

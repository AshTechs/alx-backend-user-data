#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import re
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

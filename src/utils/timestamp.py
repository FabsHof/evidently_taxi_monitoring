from datetime import datetime
import regex
import os
from os import path

def remove_timestamp_from_string(input_str: str, include_ms: bool = True) -> str:
    '''
    Removes timestamp in isoformat from a given string. The timestamp is expected to be in the format '_YYYY-MM-DDTHH-MM-SS'.
    Args:
        input_str (str): The input string potentially containing a timestamp.
        include_ms (bool, optional): Whether to include milliseconds in the timestamp. Defaults to False.
    Returns:
        str: The string with the timestamp removed.
    '''
    regexp = r'_\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}'
    if include_ms:
        regexp += r'-\d{3}'
    return regex.sub(regexp, '', input_str)

def add_current_timestamp_to_string(base_str: str, include_ms: bool = True) -> str:
    '''
    Appends the current timestamp in isoformat to a given string.
    Args:
        base_str (str): The base string to which the timestamp will be appended.
        include_ms (bool, optional): Whether to include milliseconds in the timestamp. Defaults to True.
    Returns:
        str: The string with the current timestamp appended.
    '''
    current_timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    if include_ms:
        current_timestamp += f'-{int(datetime.now().microsecond / 1000):03d}'
    return f'{base_str}_{current_timestamp}'

def remove_timestamp_from_filename(filename: str, include_ms: bool = True) -> str:
    '''
    Removes timestamp in isoformat from a given filename. The timestamp is expected to be in the format '_YYYY-MM-DDTHH-MM-SS'.
    Args:
        filename (str): The filename potentially containing a timestamp.
        include_ms (bool, optional): Whether to include milliseconds in the timestamp. Defaults to False.
    Returns:
        str: The filename with the timestamp removed.
    '''
    pathname, ext = path.splitext(filename)
    pathname_no_timestamp = remove_timestamp_from_string(pathname, include_ms=include_ms)
    return f'{pathname_no_timestamp}{ext}'

def add_current_timestamp_to_filename(filename: str, include_ms: bool = True) -> str:
    '''
    Appends the current timestamp in isoformat to a given filename.
    Args:
        filename (str): The base filename to which the timestamp will be appended.
        include_ms (bool, optional): Whether to include milliseconds in the timestamp. Defaults to True.
    Returns:
        str: The filename with the current timestamp appended.
    '''
    pathname, ext = path.splitext(filename)
    pathname = remove_timestamp_from_filename(pathname, include_ms=include_ms)
    return f'{add_current_timestamp_to_string(pathname, include_ms=include_ms)}{ext}'
"""
 fatamorgana

 fatamorgana is a python package for reading and writing to the
  OASIS layout format. The OASIS format ('.oas') is the successor to
  GDSII ('.gds') and boasts
     - Additional primitive shapes
     - Arbitrary-length integers and fractions
     - Extra ways to represent arrays of repeated shapes
     - Better support for arbitrary ASCII text data
     - More compact data storage format
     - Inline compression

 fatamorana is written in pure python and only optionally depends on
  numpy to speed up reading/writing.

 Dependencies:
    - Python 3.5 or later
    - numpy (optional, faster but no additional functionality)

 To get started, try:
 ```python3
    import fatamorgana
    help(fatamorgana.OasisLayout)
 ```
"""
import pathlib

from .main import OasisLayout, Cell, XName
from .basic import (
    NString, AString, Validation, OffsetTable, OffsetEntry,
    EOFError, SignedError, InvalidDataError, InvalidRecordError,
    UnfilledModalError,
    ReuseRepetition, GridRepetition, ArbitraryRepetition
    )


__author__ = 'Jan Petykiewicz'

from .VERSION import __version__
version = __version__

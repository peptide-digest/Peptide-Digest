"""
Unit and regression test for the peptidedigest package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import peptidedigest


def test_peptidedigest_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "peptidedigest" in sys.modules

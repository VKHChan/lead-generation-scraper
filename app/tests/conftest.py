"""
Pytest configuration and shared fixtures
"""
import os
import shutil

import pytest


def pytest_sessionfinish(session, exitstatus):
    """Clean up after all tests are done"""
    # Get project root directory (two levels up from tests)
    root_dir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Clean up __pycache__ directories
        if '__pycache__' in dirnames:
            cache_dir = os.path.join(dirpath, '__pycache__')
            shutil.rmtree(cache_dir)
            print(f"Cleaned up {cache_dir}")

        # Clean up MagicMock directories
        if 'MagicMock' in dirnames:
            mock_dir = os.path.join(dirpath, 'MagicMock')
            shutil.rmtree(mock_dir)
            print(f"Cleaned up {mock_dir}")

    # Also check root directory directly
    magic_mock_root = os.path.join(root_dir, 'MagicMock')
    if os.path.exists(magic_mock_root):
        shutil.rmtree(magic_mock_root)
        print(f"Cleaned up {magic_mock_root}")

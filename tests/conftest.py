import pytest
import sys
import os

# Add the project root to the Python path so imports work correctly
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def pytest_configure(config):
    # Example global pytest configuration hook
    config.addinivalue_line("markers", "integration: mark integration tests")

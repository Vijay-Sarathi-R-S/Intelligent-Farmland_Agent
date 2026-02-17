import pytest

def pytest_configure(config):
    # Example global pytest configuration hook
    config.addinivalue_line("markers", "integration: mark integration tests")

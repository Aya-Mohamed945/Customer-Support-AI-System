# backend/tests/conftest.py
"""
Pytest Configuration
"""

import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_ticket():
    """Sample ticket for testing"""
    return {
        "title": "Payment was charged twice",
        "description": "My card was charged twice for the same order",
        "resolution_time": 4
    }

@pytest.fixture
def sample_billing_ticket():
    """Sample billing ticket"""
    return {
        "title": "I was charged twice",
        "description": "I was charged twice for the same order",
        "resolution_time": 2
    }

@pytest.fixture
def sample_technical_ticket():
    """Sample technical ticket"""
    return {
        "title": "App crashes on startup",
        "description": "The app crashes immediately on startup",
        "resolution_time": 24
    }

@pytest.fixture
def sample_account_ticket():
    """Sample account ticket"""
    return {
        "title": "Cannot login to my account",
        "description": "I cannot login to my account",
        "resolution_time": 1
    }

@pytest.fixture
def sample_delivery_ticket():
    """Sample delivery ticket"""
    return {
        "title": "My package never arrived",
        "description": "The package never arrived",
        "resolution_time": 48
    }
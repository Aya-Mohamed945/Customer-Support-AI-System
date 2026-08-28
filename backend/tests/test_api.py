# backend/tests/test_api.py
"""
Integration Tests for API Endpoints
"""

import pytest
import requests
import json
import os
import sys

BASE_URL = "http://localhost:8000"


class TestHealth:
    """Test health endpoints"""
    
    def test_health_check(self):
        """Test health endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert data['status'] == 'healthy'
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_root(self):
        """Test root endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'message' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")


class TestPrediction:
    """Test prediction endpoint"""
    
    def test_predict_success(self):
        """Test successful prediction"""
        try:
            data = {
                "title": "Payment was charged twice",
                "description": "My card was charged twice for the same order",
                "resolution_time": 4
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                json=data,
                timeout=30
            )
            assert response.status_code == 200
            result = response.json()
            assert 'category' in result
            assert 'priority' in result
            assert 'sentiment' in result
            assert 'suggested_solution' in result
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_predict_billing(self):
        """Test billing ticket prediction"""
        try:
            data = {
                "title": "I was charged twice",
                "description": "I was charged twice for the same order",
                "resolution_time": 2
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                json=data,
                timeout=30
            )
            assert response.status_code == 200
            result = response.json()
            assert result['category'] == 'billing'
            assert result['priority'] in ['High', 'Medium', 'Low']
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_predict_technical(self):
        """Test technical ticket prediction"""
        try:
            data = {
                "title": "App crashes on startup",
                "description": "The app crashes immediately on startup",
                "resolution_time": 24
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                json=data,
                timeout=30
            )
            assert response.status_code == 200
            result = response.json()
            assert result['category'] == 'technical'
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_predict_account(self):
        """Test account ticket prediction"""
        try:
            data = {
                "title": "Cannot login to my account",
                "description": "I cannot login to my account",
                "resolution_time": 1
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                json=data,
                timeout=30
            )
            assert response.status_code == 200
            result = response.json()
            assert result['category'] == 'account'
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_predict_delivery(self):
        """Test delivery ticket prediction"""
        try:
            data = {
                "title": "My package never arrived",
                "description": "The package never arrived",
                "resolution_time": 48
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/predict",
                json=data,
                timeout=30
            )
            assert response.status_code == 200
            result = response.json()
            assert result['category'] == 'delivery'
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")


class TestMetrics:
    """Test metrics endpoints"""
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        try:
            response = requests.get(f"{BASE_URL}/api/v1/metrics", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert 'total_predictions' in data
            assert 'uptime_hours' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_recent_tickets(self):
        """Test recent tickets endpoint"""
        try:
            response = requests.get(
                f"{BASE_URL}/api/v1/metrics/tickets/recent",
                timeout=5
            )
            assert response.status_code == 200
            data = response.json()
            assert 'tickets' in data
            assert 'total' in data
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")


class TestRAG:
    """Test RAG endpoints"""
    
    def test_rag_retrieve(self):
        """Test RAG retrieval"""
        try:
            data = {
                "query": "How long does a refund take?",
                "k": 2,
                "threshold": 0.1
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/rag/retrieve",
                json=data,
                timeout=10
            )
            assert response.status_code in [200, 404]
            if response.status_code == 200:
                result = response.json()
                assert 'results' in result
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")


class TestAuth:
    """Test authentication endpoints"""
    
    def test_signup(self):
        """Test signup endpoint"""
        try:
            data = {
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/signup",
                json=data,
                timeout=10
            )
            # 200 = success, 400 = already exists
            assert response.status_code in [200, 400]
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
    
    def test_login(self):
        """Test login endpoint"""
        try:
            data = {
                "email": "test@example.com",
                "password": "password123"
            }
            response = requests.post(
                f"{BASE_URL}/api/v1/auth/login",
                json=data,
                timeout=10
            )
            # 200 = success, 401 = invalid
            assert response.status_code in [200, 401]
        except requests.exceptions.ConnectionError:
            pytest.skip("API not running")
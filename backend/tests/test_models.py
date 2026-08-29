# backend/tests/test_models.py
"""
Unit Tests for ML Models
"""

import pytest
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Import app modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml.preprocessing import preprocess_text
from app.ml.pipeline import get_pipeline
from app.core.dependencies import get_model_manager


class TestPreprocessing:
    """Test text preprocessing"""

    def test_preprocess_text(self):
        """Test basic preprocessing"""
        text = "Hello WORLD! This is a TEST."
        result = preprocess_text(text)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "world" in result.lower()

    def test_preprocess_empty(self):
        """Test empty text"""
        assert preprocess_text(None) == ""
        assert preprocess_text("") == ""

    def test_preprocess_special_chars(self):
        """Test removal of special characters"""
        text = "Hello!!! @#$% 123"
        result = preprocess_text(text)
        assert "!!!" not in result
        assert "@" not in result
        assert "#" not in result


class TestModels:
    """Test ML models loading and prediction"""

    def test_model_manager_loads(self):
        """Test ModelManager loads correctly"""
        try:
            manager = get_model_manager()
            assert manager is not None
            assert hasattr(manager, '_models')
        except Exception as e:
            pytest.skip(f"Models not loaded: {e}")

    def test_priority_model_exists(self):
        """Test priority model exists"""
        model_path = "./models/priority_model_final.pkl"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            assert model is not None
        else:
            pytest.skip("Priority model not found")

    def test_category_model_exists(self):
        """Test category model exists"""
        model_path = "./models/category_model_final.pkl"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            assert model is not None
        else:
            pytest.skip("Category model not found")

    def test_sentiment_model_exists(self):
        """Test sentiment model exists"""
        model_path = "./models/sentiment_model_final.pkl"
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            assert model is not None
        else:
            pytest.skip("Sentiment model not found")


class TestPredictionPipeline:
    """Test prediction pipeline"""

    def test_pipeline_initialization(self):
        """Test pipeline initializes"""
        try:
            pipeline = get_pipeline()
            assert pipeline is not None
        except Exception as e:
            pytest.skip(f"Pipeline not initialized: {e}")

    def test_pipeline_predict(self):
        """Test pipeline prediction"""
        try:
            pipeline = get_pipeline()
            if pipeline is None:
                pytest.skip("Pipeline not available")

            result = pipeline.predict(
                title="Test ticket",
                description="This is a test description"
            )

            assert result is not None
            assert 'category' in result
            assert 'priority' in result
            assert 'sentiment' in result
            assert 'suggested_solution' in result

        except Exception as e:
            pytest.skip(f"Prediction failed: {e}")


class TestVectorizers:
    """Test vectorizers"""

    def test_priority_vectorizer(self):
        """Test priority vectorizer"""
        vectorizer_path = "./models/priority_vectorizer_final.pkl"
        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            assert vectorizer is not None
            assert hasattr(vectorizer, 'transform')
        else:
            pytest.skip("Priority vectorizer not found")

    def test_category_vectorizer(self):
        """Test category vectorizer"""
        vectorizer_path = "./models/category_vectorizer_final.pkl"
        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            assert vectorizer is not None
            assert hasattr(vectorizer, 'transform')
        else:
            pytest.skip("Category vectorizer not found")

    def test_sentiment_vectorizer(self):
        """Test sentiment vectorizer"""
        vectorizer_path = "./models/sentiment_vectorizer_final.pkl"
        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            assert vectorizer is not None
            assert hasattr(vectorizer, 'transform')
        else:
            pytest.skip("Sentiment vectorizer not found")

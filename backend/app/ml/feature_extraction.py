# app/ml/feature_extraction.py
import numpy as np
import re
from typing import Optional


def extract_advanced_features(text: str) -> np.ndarray:
    """
    Extract advanced features for priority prediction
    
    Args:
        text: Input text string
        
    Returns:
        Numpy array of features
    """
    text = str(text).lower()
    words = text.split()
    
    # Length features
    text_len = len(text)
    word_count = len(words)
    avg_word_len = text_len / (word_count + 1) if word_count > 0 else 0
    
    # Urgency keywords
    urgency_words = [
        'urgent', 'immediately', 'asap', 'emergency', 'critical',
        'broken', 'down', 'not working', 'issue', 'problem',
        'help', 'stuck', 'blocked', 'error', 'fail', 'crash'
    ]
    urgency_count = sum(1 for w in urgency_words if w in text)
    
    # Money keywords
    money_words = [
        'money', 'payment', 'charge', 'billing', 'invoice',
        'refund', 'dollar', '$', 'price', 'cost', 'fee'
    ]
    money_count = sum(1 for w in money_words if w in text)
    
    # Account keywords
    account_words = [
        'account', 'login', 'password', 'access', 'suspended',
        'locked', 'blocked', 'security', 'verify'
    ]
    account_count = sum(1 for w in account_words if w in text)
    
    # Technical keywords
    tech_words = [
        'app', 'website', 'error', 'bug', 'crash', 'freeze',
        'load', 'slow', 'performance', 'server'
    ]
    tech_count = sum(1 for w in tech_words if w in text)
    
    # Punctuation
    exclamation_count = text.count('!')
    question_count = text.count('?')
    
    # Capitalization (urgency/anger indicator)
    caps_count = sum(1 for w in words if w.isupper() and len(w) > 2)
    
    # Numerical values
    number_count = len(re.findall(r'\d+', text))
    
    return np.array([[
        text_len,
        word_count,
        avg_word_len,
        urgency_count,
        money_count,
        account_count,
        tech_count,
        exclamation_count,
        question_count,
        caps_count,
        number_count
    ]])


def extract_resolution_features(resolution_time: Optional[float]) -> np.ndarray:
    """
    Extract resolution time features
    
    Args:
        resolution_time: Resolution time in hours
        
    Returns:
        Numpy array of features
    """
    if resolution_time is None or np.isnan(resolution_time):
        resolution_time = 24  # Default medium
    
    # Categorize resolution time
    if resolution_time <= 12:
        res_cat = 0  # High priority (fast resolution)
    elif resolution_time <= 48:
        res_cat = 1  # Medium priority
    else:
        res_cat = 2  # Low priority (slow resolution)
    
    # Normalize resolution time
    res_normalized = resolution_time / 168  # Max 168 hours (7 days)
    
    return np.array([[res_cat, res_normalized]])
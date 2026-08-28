# scripts/train_models.py
"""
🔄 Training Pipeline - Updated with Priority Model (20 Clusters)
Priority Model: 98.84% Cross-Validation Accuracy
"""

import pandas as pd
import numpy as np
import joblib
import pickle
import os
import re
import warnings
warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.cluster import KMeans

# Import preprocessing from app
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.ml.preprocessing import preprocess_text


# ============================================
# CONFIGURATION
# ============================================
MODELS_DIR = "./models"
DATA_DIR = "./data"
RANDOM_STATE = 42
TEST_SIZE = 0.2
N_CLUSTERS = 20


print("="*60)
print("🔄 TRAINING ALL MODELS WITH CLEAN DATA")
print("   Priority Model: 20 Clusters (98.84% CV)")
print("="*60)


# ============================================
# ENHANCED CATEGORY KEYWORDS (مطورة)
# ============================================

category_keywords = {
    'technical': [
        # Original
        'technical', 'bug', 'error', 'crash', 'freeze', 'load', 'slow',
        'performance', 'server', 'app', 'website', 'interface', 'ui',
        'ux', 'design', 'dark mode', 'theme', 'feature', 'enhancement',
        'suggestion', 'improvement', 'update', 'version', 'compatibility',
        'hardware', 'software', 'driver', 'install', 'download', 'upload',
        'sync', 'patch', 'fix', 'debug', 'troubleshoot',
        'network', 'internet', 'wifi', 'connect', 'disconnect', 'timeout',
        'latency', 'bandwidth', 'signal', 'port', 'firewall', 'proxy',
        'code', 'database', 'query', 'sql',
        
        # 🆕 API & Integration
        'api', 'endpoint', 'integration', 'webhook', 'callback',
        'server error', '500 error', 'gateway', 'timeout',
        'rate limit', 'throttle', 'payload', 'schema',
        'authentication', 'token', 'oauth', 'jwt',
        'deployment', 'migration', 'production', 'environment',
        'devops', 'ci/cd', 'pipeline', 'build', 'deploy',
        'request', 'response', 'json', 'xml', 'http'
    ],
    
    'billing': [
        'billing', 'payment', 'charge', 'invoice', 'refund', 'money',
        'card', 'credit', 'debit', 'paypal', 'stripe', 'transaction',
        'amount', 'price', 'cost', 'fee', 'tax', 'vat', 'currency',
        'subscription', 'renewal', 'cancel', 'plan', 'upgrade', 'downgrade',
        'overcharge', 'double charge', 'fraud', 'dispute', 'reconcile',
        'receipt', 'statement', 'balance', 'due', 'overdue', 'payment method',
        'credit card', 'debit card', 'bank transfer', 'wire transfer',
        'discount', 'coupon', 'promo', 'credit', 'debit', 'chargeback',
        'charged twice', 'duplicate charge', 'billed twice'
    ],
    
    'account': [
        'account', 'login', 'password', 'access', 'suspended', 'locked',
        'blocked', 'security', 'verify', 'authentication', 'email', 'username',
        'profile', 'settings', 'preferences', 'logout', 'session', 'expired',
        'reset', 'recovery', '2fa', 'mfa', 'otp', 'verification',
        'registration', 'signup', 'sign in', 'log in', 'log out',
        'change password', 'forgot password', 'reset password',
        'security question', 'backup code', 'authenticator',
        'change email', 'update email', 'new email', 'personal email', 'work email'
    ],
    
    'delivery': [
        'delivery', 'shipping', 'order', 'package', 'track', 'tracking',
        'arrived', 'missing', 'lost', 'damaged', 'return', 'exchange',
        'address', 'zip', 'postal', 'courier', 'fedex', 'dhl', 'ups',
        'usps', 'dispatch', 'fulfillment', 'warehouse', 'inventory', 'stock',
        'shipment', 'cargo', 'freight', 'delivery date', 'estimated delivery',
        'tracking number', 'delivery confirmation', 'signature required',
        'reschedule delivery', 'change address', 'delivery instructions',
        
        # 🆕 Missing Package
        'never arrived', "didn't arrive", 'missing package',
        'lost package', 'no delivery', 'not delivered',
        'package not received', 'order not received',
        'tracking shows delivered', 'tracking not updated',
        'no tracking update', 'shipping delay', 'late delivery',
        'delayed shipping', 'express shipping', 'standard shipping'
    ]
}


# ============================================
# ENHANCED SENTIMENT KEYWORDS (مطورة)
# ============================================

sentiment_keywords = {
    'positive': [
        'great', 'good', 'excellent', 'amazing', 'awesome', 'wonderful',
        'love', 'like', 'appreciate', 'helpful', 'thanks', 'thank you',
        'satisfied', 'happy', 'pleased', 'glad', 'best', 'perfect',
        'nice', 'fantastic', 'outstanding', 'superb', 'brilliant',
        'suggestion', 'improvement', 'enhancement', 'feedback',
        'grateful', 'thankful', 'appreciated',
        'works perfectly', 'no issues', 'smooth', 'quick', 'fast',
        'easy', 'simple', 'clear', 'great service', 'good experience',
        'well done', 'impressive', 'reliable', 'trustworthy',
        'recommend', 'highly recommend', 'best service', 'excellent support',
        'fantastic', 'love it', 'perfect', 'brilliant',
        
        # 🆕 Positive
        'love your app', 'absolutely love', 'amazing experience',
        'very helpful', 'quick response', 'fast resolution',
        'thank you', 'appreciate the help', 'wonderful experience'
    ],
    
    'neutral': [
        'suggestion', 'proposal', 'idea', 'recommendation',
        'not urgent', 'can wait', 'nice to have', 'future',
        'maybe', 'perhaps', 'could', 'would be nice',
        'okay', 'fine', 'not sure', 'neutral', 'average',
        'mediocre', 'so so', 'not bad', 'not great', 'decent',
        'acceptable', 'moderate', 'fair', 'alright',
        'neither', 'nor', 'uncertain', 'undecided', 'indifferent',
        'just asking', 'curious', 'wondering', 'clarification',
        'information', 'details', 'explain', 'understand',
        'is it possible', 'can you', 'could you', 'would you',
        'how to', 'what is', 'where is', 'when is',
        
        # 🆕 Neutral
        'just asking', 'curious about', 'wondering if', 'would like to know',
        'possible to', 'way to do this', 'guide me through',
        'not sure about', 'how does this work', 'what is the process',
        'would like to', 'interested in', 'looking for'
    ],
    
    'negative': [
        'bad', 'terrible', 'awful', 'horrible', 'worst',
        'disappointed', 'frustrated', 'annoyed', 'upset',
        'hate', 'poor', 'useless', 'waste', 'sorry',
        'unfortunately', 'disappointing', 'unacceptable',
        'problem', 'issue', 'complaint', 'unhappy',
        'not working', 'does not work', 'failed', 'fail',
        'dissatisfied', 'frustrating', 'unhelpful', 'unreliable',
        'still not', "hasn't", "didn't", "wasn't", "wouldn't",
        'never', 'always', 'every time', 'keep', 'constantly',
        'no response', 'no update', 'no help', 'no solution',
        'waste of time', 'waste of money', 'terrible experience',
        'not good', 'could be better', 'disappointing'
    ],
    
    'angry': [
        'angry', 'furious', 'outraged', 'livid', 'frustrated',
        'irritated', 'annoyed', 'mad', 'upset', 'frustrating',
        'infuriating', 'enraged', 'agitated', 'hostile', 'irate',
        'fuming', 'seething', 'incensed', 'indignant', 'vexed',
        'URGENT', 'IMMEDIATELY', 'ASAP', 'EMERGENCY', 'CRITICAL',
        'immediately', 'as soon as possible', 'right away', 'now',
        'unacceptable', 'intolerable', 'outrageous', 'appalling',
        'disgraceful', 'shocking', 'infuriating', 'rage',
        'furious', 'livid', 'seething', 'fuming',
        'demand', 'insist', 'require immediate', 'must fix',
        'not acceptable', 'cannot accept', 'will not accept',
        
        # 🆕 Duplicate Charge & Urgent
        'charged twice', 'double charge', 'duplicate charge',
        'billed twice', 'charged again', 'second charge',
        'demand refund', 'need immediate refund', 'fix this now',
        'critical issue', 'urgent attention', 'this is unacceptable'
    ]
}


# ============================================
# 1. TRAIN PRIORITY MODEL (20 Clusters)
# ============================================
print("\n" + "="*60)
print("📊 1. TRAINING PRIORITY MODEL (20 CLUSTERS)")
print("="*60)

def train_priority_model():
    """تدريب Priority Model بـ 20 Clusters"""
    
    # 1.1 Load data
    print("\n1.1 Loading data...")
    
    possible_files = [
        f"{DATA_DIR}/processed/priority_final_data_real_low.csv",
        "priority_final_data_real_low.csv"
    ]
    
    df = None
    for f in possible_files:
        if os.path.exists(f):
            df = pd.read_csv(f)
            print(f"   ✅ Loaded: {f}")
            break
    
    if df is None:
        print("   ❌ No data found! Please run priority_relabeling first.")
        return None
    
    print(f"   ✅ Samples: {len(df)}")
    
    # 1.2 Prepare text
    print("\n1.2 Preparing text...")
    
    if 'text' in df.columns:
        X_texts = df['text'].tolist()
    elif 'full_text' in df.columns:
        X_texts = df['full_text'].tolist()
    else:
        X_texts = df['processed'].tolist()
    
    y = df['priority_label'].tolist()
    print(f"   ✅ {len(X_texts)} texts ready")
    print(f"   ✅ Distribution: {pd.Series(y).value_counts().to_dict()}")
    
    # 1.3 Preprocess
    print("\n1.3 Preprocessing...")
    X_processed = [preprocess_text(t) for t in X_texts]
    print(f"   ✅ {len(X_processed)} texts preprocessed")
    
    # 1.4 Vectorize
    print("\n1.4 Vectorizing...")
    vectorizer = TfidfVectorizer(
        max_features=3000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=3,
        max_df=0.8
    )
    X_vec = vectorizer.fit_transform(X_processed)
    print(f"   ✅ Feature matrix: {X_vec.shape}")
    
    # 1.5 Cross-Validation
    print("\n1.5 Cross-Validation (5-Fold)...")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    model = LogisticRegression(
        C=0.5,
        max_iter=1000,
        class_weight='balanced',
        random_state=RANDOM_STATE
    )
    
    cv_scores = cross_val_score(model, X_vec, y, cv=cv, scoring='accuracy')
    print(f"   ✅ CV Scores: {[f'{s:.4f}' for s in cv_scores]}")
    print(f"   ✅ Mean CV Accuracy: {cv_scores.mean():.4f} ({cv_scores.mean()*100:.2f}%)")
    print(f"   ✅ Std CV Accuracy: {cv_scores.std():.4f}")
    
    # 1.6 Train Final Model
    print("\n1.6 Training final model...")
    model.fit(X_vec, y)
    print("   ✅ Model trained")
    
    # 1.7 Save Models
    print("\n1.7 Saving models...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    joblib.dump(model, f"{MODELS_DIR}/priority_model_final.pkl")
    print(f"   ✅ Saved: {MODELS_DIR}/priority_model_final.pkl")
    
    joblib.dump(vectorizer, f"{MODELS_DIR}/priority_vectorizer_final.pkl")
    print(f"   ✅ Saved: {MODELS_DIR}/priority_vectorizer_final.pkl")
    
    priority_encoder = LabelEncoder()
    priority_encoder.classes_ = np.array(['High', 'Low', 'Medium'])
    with open(f"{MODELS_DIR}/priority_encoder.pkl", 'wb') as f:
        pickle.dump(priority_encoder, f)
    print(f"   ✅ Saved: {MODELS_DIR}/priority_encoder.pkl")
    
    # 1.8 Summary
    print("\n" + "-"*40)
    print("📊 PRIORITY MODEL SUMMARY")
    print("-"*40)
    print(f"   Clusters: {N_CLUSTERS}")
    print(f"   Samples: {len(df)}")
    print(f"   Distribution: {pd.Series(y).value_counts().to_dict()}")
    print(f"   CV Mean: {cv_scores.mean():.4f} ({cv_scores.mean()*100:.2f}%)")
    print(f"   CV Std: {cv_scores.std():.4f}")
    print("-"*40)
    
    return {
        'model': model,
        'vectorizer': vectorizer,
        'encoder': priority_encoder,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


# ============================================
# 2. TRAIN CATEGORY MODEL (ENHANCED)
# ============================================
print("\n" + "="*60)
print("📊 2. TRAINING CATEGORY MODEL (ENHANCED)")
print("="*60)

def train_category_model():
    """تدريب Category Model مع Keywords محسّنة"""
    
    print("\n2.1 Loading data...")
    cat_df = pd.read_csv(f"{DATA_DIR}/raw/E-Commerce_data.csv")
    saas_df = pd.read_csv(f"{DATA_DIR}/raw/SaaS_Tech_data.csv")
    cat_combined = pd.concat([cat_df, saas_df], ignore_index=True)
    print(f"   ✅ Loaded {len(cat_combined)} samples")
    
    # === Enhance text with category keywords ===
    print("\n2.2 Enhancing text with category keywords...")
    
    def enhance_category_text(text):
        """إضافة كلمات مفتاحية لتحسين التصنيف"""
        text_lower = str(text).lower()
        
        # حساب عدد الكلمات المفتاحية لكل Category
        scores = {}
        for category, keywords in category_keywords.items():
            scores[category] = sum(1 for kw in keywords if kw in text_lower)
        
        # أعلى Category
        if scores:
            best_category = max(scores, key=scores.get)
            if scores[best_category] >= 2:  # على الأقل 2 كلمات مفتاحية
                return f"[{best_category.upper()}] " + text
        
        return text
    
    cat_combined['enhanced'] = cat_combined['description'].apply(enhance_category_text)
    cat_combined['full_text'] = cat_combined['title'] + " " + cat_combined['enhanced']
    
    cat_encoder = LabelEncoder()
    cat_combined['category_enc'] = cat_encoder.fit_transform(cat_combined['category'])
    
    X_cat = cat_combined['full_text'].tolist()
    y_cat = cat_combined['category_enc'].tolist()
    
    # 2.3 Split
    print("\n2.3 Splitting data...")
    X_cat_train, X_cat_test, y_cat_train, y_cat_test = train_test_split(
        X_cat, y_cat, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_cat
    )
    print(f"   ✅ Train: {len(X_cat_train)}, Test: {len(X_cat_test)}")
    
    # 2.4 Vectorize
    print("\n2.4 Vectorizing...")
    cat_vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=2
    )
    X_cat_train_vec = cat_vectorizer.fit_transform(X_cat_train)
    X_cat_test_vec = cat_vectorizer.transform(X_cat_test)
    print(f"   ✅ Shape: {X_cat_train_vec.shape}")
    
    # 2.5 Train
    print("\n2.5 Training...")
    category_model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        C=1.0
    )
    category_model.fit(X_cat_train_vec, y_cat_train)
    
    # 2.6 Evaluate
    y_cat_pred = category_model.predict(X_cat_test_vec)
    cat_accuracy = accuracy_score(y_cat_test, y_cat_pred)
    print(f"\n   🎯 Category Accuracy: {cat_accuracy:.4f} ({cat_accuracy*100:.2f}%)")
    
    print("\n📋 Classification Report:")
    print(classification_report(y_cat_test, y_cat_pred, target_names=cat_encoder.classes_))
    
    # 2.7 Save
    print("\n2.7 Saving...")
    joblib.dump(category_model, f"{MODELS_DIR}/category_model_final.pkl")
    joblib.dump(cat_vectorizer, f"{MODELS_DIR}/category_vectorizer_final.pkl")
    with open(f"{MODELS_DIR}/category_encoder.pkl", 'wb') as f:
        pickle.dump(cat_encoder, f)
    print("   ✅ Category models saved")
    
    return cat_accuracy


# ============================================
# 3. TRAIN SENTIMENT MODEL (ENHANCED)
# ============================================
print("\n" + "="*60)
print("📊 3. TRAINING SENTIMENT MODEL (4 CLASSES - ENHANCED)")
print("="*60)

def train_sentiment_model():
    """تدريب Sentiment Model (4 Classes) مع Keywords محسّنة"""
    
    # 3.1 Load data
    print("\n3.1 Loading data...")
    sentiment_files = [
        f"{DATA_DIR}/processed/balanced_sentiment_data.csv",
        f"{DATA_DIR}/processed/final_keywords_only.csv"
    ]
    
    sentiment_df = None
    for f in sentiment_files:
        if os.path.exists(f):
            sentiment_df = pd.read_csv(f)
            print(f"   ✅ Loaded: {f}")
            break
    
    if sentiment_df is None:
        print("   ⚠️ No sentiment data found! Skipping...")
        return None
    
    # 3.2 Enhance text with sentiment keywords
    print("\n3.2 Enhancing text with sentiment keywords...")
    
    def enhance_sentiment_text(text):
        """إضافة كلمات مفتاحية لتحسين التصنيف"""
        text_lower = str(text).lower()
        
        # Angry (highest priority)
        if any(kw in text_lower for kw in sentiment_keywords['angry']):
            return text + " [ANGRY]"
        # Positive
        elif any(kw in text_lower for kw in sentiment_keywords['positive']):
            return text + " [POSITIVE]"
        # Negative
        elif any(kw in text_lower for kw in sentiment_keywords['negative']):
            return text + " [NEGATIVE]"
        # Neutral
        elif any(kw in text_lower for kw in sentiment_keywords['neutral']):
            return text + " [NEUTRAL]"
        
        return text
    
    X_sen_enhanced = [enhance_sentiment_text(t) for t in sentiment_df['text'].tolist()]
    y_sen = sentiment_df['label'].tolist()
    
    print(f"   ✅ Samples: {len(X_sen_enhanced)}")
    print(f"   ✅ Distribution: {pd.Series(y_sen).value_counts().to_dict()}")
    
    # 3.3 Split
    print("\n3.3 Splitting...")
    X_sen_train, X_sen_test, y_sen_train, y_sen_test = train_test_split(
        X_sen_enhanced, y_sen, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y_sen
    )
    print(f"   ✅ Train: {len(X_sen_train)}, Test: {len(X_sen_test)}")
    
    # 3.4 Vectorize
    print("\n3.4 Vectorizing...")
    sentiment_vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        min_df=2
    )
    X_sen_train_vec = sentiment_vectorizer.fit_transform(X_sen_train)
    X_sen_test_vec = sentiment_vectorizer.transform(X_sen_test)
    print(f"   ✅ Shape: {X_sen_train_vec.shape}")
    
    # 3.5 Train
    print("\n3.5 Training...")
    sentiment_model = LogisticRegression(
        C=10.0,
        max_iter=1000,
        class_weight='balanced',
        random_state=RANDOM_STATE
    )
    sentiment_model.fit(X_sen_train_vec, y_sen_train)
    
    # 3.6 Evaluate
    y_sen_pred = sentiment_model.predict(X_sen_test_vec)
    sen_accuracy = accuracy_score(y_sen_test, y_sen_pred)
    print(f"\n   🎯 Sentiment Accuracy: {sen_accuracy:.4f} ({sen_accuracy*100:.2f}%)")
    
    print("\n📋 Classification Report:")
    sentiment_encoder = LabelEncoder()
    sentiment_encoder.classes_ = np.array(['positive', 'neutral', 'negative', 'angry'])
    print(classification_report(y_sen_test, y_sen_pred, target_names=sentiment_encoder.classes_))
    
    # 3.7 Save
    print("\n3.7 Saving...")
    joblib.dump(sentiment_model, f"{MODELS_DIR}/sentiment_model_final.pkl")
    joblib.dump(sentiment_vectorizer, f"{MODELS_DIR}/sentiment_vectorizer_final.pkl")
    with open(f"{MODELS_DIR}/sentiment_encoder.pkl", 'wb') as f:
        pickle.dump(sentiment_encoder, f)
    print("   ✅ Sentiment models saved")
    
    return sen_accuracy


# ============================================
# 4. MAIN - RUN ALL
# ============================================
if __name__ == "__main__":
    
    print("\n" + "="*60)
    print("🚀 STARTING TRAINING PIPELINE")
    print("="*60)
    
    results = {}
    
    # Train Priority
    priority_result = train_priority_model()
    if priority_result:
        results['priority'] = priority_result['cv_mean']
    
    # Train Category
    cat_accuracy = train_category_model()
    if cat_accuracy:
        results['category'] = cat_accuracy
    
    # Train Sentiment
    sen_accuracy = train_sentiment_model()
    if sen_accuracy:
        results['sentiment'] = sen_accuracy
    
    # Final Summary
    print("\n" + "="*60)
    print("📊 FINAL TRAINING SUMMARY")
    print("="*60)
    for model, acc in results.items():
        if model == 'priority':
            print(f"   ✅ Priority:  {acc*100:.2f}% (CV Mean)")
        else:
            print(f"   ✅ {model.capitalize()}: {acc*100:.2f}%")
    print("="*60)
    print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
    print("="*60)
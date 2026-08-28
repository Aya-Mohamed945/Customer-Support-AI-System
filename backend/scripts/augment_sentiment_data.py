# scripts/augment_sentiment_data.py
"""
تضخيم بيانات Sentiment باستخدام Synonym Replacement
"""

import pandas as pd
import random
import nltk
from nltk.corpus import wordnet

# تحميل NLTK data لو مش موجود
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

def synonym_replacement(text, n=2):
    """استبدال كلمات بمرادفاتها"""
    words = text.split()
    if len(words) < 3:
        return text
    
    new_words = words.copy()
    # اختيار كلمات عشوائية للاستبدال
    random_word_list = list(set([word for word in words if wordnet.synsets(word)]))
    if len(random_word_list) == 0:
        return text
    
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = wordnet.synsets(random_word)
        if synonyms:
            synonym = synonyms[0].lemmas()[0].name().replace('_', ' ')
            if synonym != random_word:
                new_words = [synonym if word == random_word else word for word in new_words]
                num_replaced += 1
        if num_replaced >= n:
            break
    return ' '.join(new_words)

def augment_sentiment_data(df, label, multiplier=2):
    """تضخيم البيانات لفئة معينة"""
    class_data = df[df['label'] == label]
    if len(class_data) == 0:
        return pd.DataFrame()
    
    augmented = []
    for _, row in class_data.iterrows():
        for _ in range(multiplier - 1):
            new_text = synonym_replacement(row['text'], n=2)
            augmented.append({'text': new_text, 'label': label})
    
    return pd.DataFrame(augmented)

def main():
    print("="*60)
    print("📊 AUGMENTING SENTIMENT DATA")
    print("="*60)
    
    # 1. تحميل البيانات
    print("\n1. Loading data...")
    df = pd.read_csv("data/processed/balanced_sentiment_data.csv")
    print(f"   ✅ Loaded {len(df)} samples")
    print(f"   📊 Distribution: {df['label'].value_counts().to_dict()}")
    
    # 2. تضخيم الفئات الضعيفة
    print("\n2. Augmenting data...")
    
    # positive: multiplier 3 (200 → 600)
    positive_aug = augment_sentiment_data(df, 'positive', multiplier=3)
    print(f"   ✅ Positive: +{len(positive_aug)} samples")
    
    # neutral: multiplier 2 (300 → 600)
    neutral_aug = augment_sentiment_data(df, 'neutral', multiplier=2)
    print(f"   ✅ Neutral: +{len(neutral_aug)} samples")
    
    # angry: multiplier 2 (300 → 600)
    angry_aug = augment_sentiment_data(df, 'angry', multiplier=2)
    print(f"   ✅ Angry: +{len(angry_aug)} samples")
    
    # 3. دمج البيانات
    print("\n3. Merging data...")
    df_augmented = pd.concat([df, positive_aug, neutral_aug, angry_aug], ignore_index=True)
    df_augmented = df_augmented.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"   ✅ Data augmented from {len(df)} to {len(df_augmented)} samples")
    print(f"   📊 New distribution: {df_augmented['label'].value_counts().to_dict()}")
    
    # 4. حفظ البيانات
    print("\n4. Saving data...")
    df_augmented.to_csv("data/processed/balanced_sentiment_data_augmented.csv", index=False)
    print("   ✅ Saved: data/processed/balanced_sentiment_data_augmented.csv")
    
    print("\n" + "="*60)
    print("✅ DATA AUGMENTATION COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
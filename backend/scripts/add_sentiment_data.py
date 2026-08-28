# scripts/add_sentiment_data.py
"""
إضافة بيانات جديدة لـ Sentiment Model
"""

import pandas as pd
import os

print("=" * 60)
print("📊 ADDING SENTIMENT DATA")
print("=" * 60)

# تحميل البيانات الحالية
df = pd.read_csv("data/processed/balanced_sentiment_data.csv")
print(f"\n1. Current data: {len(df)} samples")

# حذف الـ NaN (إن وجد)
df = df.dropna()
print(f"   After dropping NaN: {len(df)} samples")

# البيانات الجديدة (بالأرقام الصحيحة)
# 0 = negative, 1 = neutral, 2 = positive, 3 = angry
new_data = [
    # ===== neutral (1) =====
    ("When does my subscription renew?", 1),
    ("How to change payment method?", 1),
    ("How long does refund take?", 1),
    ("Need to update billing address", 1),
    ("Where are account settings?", 1),
    ("How to turn off notifications?", 1),
    ("How to make profile private?", 1),
    ("New feature suggestion", 1),
    ("Does it work on Safari?", 1),
    ("Shipping options available", 1),
    
    # ===== positive (2) =====
    ("I love your app! It's fantastic!", 2),
    ("Great service, very helpful support!", 2),
    ("Amazing experience, highly recommend!", 2),
    ("The new feature is wonderful, thank you!", 2),
    ("Best customer service I've ever had!", 2),
    
    # ===== angry (3) =====
    ("I was charged twice! This is unacceptable!", 3),
    ("URGENT! Payment gateway is down!", 3),
    ("My card was billed twice! Need immediate refund!", 3),
    ("This is critical, fix it now!", 3),
    ("I demand a refund immediately!", 3),
]

# تحويل إلى DataFrame
new_df = pd.DataFrame(new_data, columns=['text', 'label'])

# دمج البيانات القديمة والجديدة
df = pd.concat([df, new_df], ignore_index=True)

# التأكد من مفيش NaN
print(f"\n2. After adding new data: {len(df)} samples")
print(f"   NaN values: {df.isna().sum().sum()}")

# التوزيع الجديد
print("\n3. New distribution:")
print(df['label'].value_counts().sort_index())

# حفظ
df.to_csv("data/processed/balanced_sentiment_data.csv", index=False)
print("\n✅ Data saved to: data/processed/balanced_sentiment_data.csv")
print("=" * 60)
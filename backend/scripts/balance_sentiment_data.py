# scripts/balance_sentiment_data.py

import pandas as pd
from sklearn.utils import resample

df = pd.read_csv("data/processed/balanced_sentiment_data.csv")

# شوفي التوزيع الحالي
print(df['label'].value_counts())

# تحديد الهدف: نفس عدد الـ negative (400)
target_count = 400

# زيادة positive من 200 → 400
positive = df[df['label'] == 'positive']
positive_aug = resample(positive, replace=True, n_samples=target_count, random_state=42)

# زيادة neutral من 300 → 400
neutral = df[df['label'] == 'neutral']
neutral_aug = resample(neutral, replace=True, n_samples=target_count, random_state=42)

# angry من 300 → 400
angry = df[df['label'] == 'angry']
angry_aug = resample(angry, replace=True, n_samples=target_count, random_state=42)

# negative موجود بالفعل 400
negative = df[df['label'] == 'negative']

# دمج الكل
balanced_df = pd.concat([positive_aug, neutral_aug, angry_aug, negative])

# خلط
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

print(balanced_df['label'].value_counts())
# positive: 400, neutral: 400, angry: 400, negative: 400 ✅

balanced_df.to_csv("data/processed/balanced_sentiment_data.csv", index=False)
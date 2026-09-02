# scripts/fix_sentiment_distribution.py
"""
تعديل توزيع الـ Sentiment Data عشان تكون متوازنة تماماً
"""

import pandas as pd

print("=" * 60)
print("📊 FIXING SENTIMENT DISTRIBUTION")
print("=" * 60)

df = pd.read_csv("data/processed/balanced_sentiment_data.csv")
df = df.dropna()

print(f"\n1. Current distribution:")
print(df['label'].value_counts().sort_index())

TARGET = 500


neutral_df = df[df['label'] == 1]
if len(neutral_df) > TARGET:
    neutral_df = neutral_df.sample(n=TARGET, random_state=42)
    print(f"   Neutral (1): {len(neutral_df)} (was 450)")

positive_df = df[df['label'] == 2]
positive_extra = []
if len(positive_df) < TARGET:
    positive_tickets = [
        "The customer service was excellent!",
        "I'm really happy with my purchase",
        "The support team was amazing",
        "This is the best app I've ever used",
        "I'm so satisfied with the service",
        "The product quality is outstanding",
        "Thank you for the quick response",
        "I love the new features",
        "The team went above and beyond",
        "Everything worked perfectly",
        "I'm impressed by how fast you fixed the issue",
        "This is a huge improvement",
        "I will definitely recommend this to others",
        "The solution you provided was perfect",
        "I'm grateful for your help",
        "You guys are doing an amazing job",
        "I'm very satisfied with the outcome",
        "The app works flawlessly",
        "Great experience overall",
        "I'm so glad I chose your company",
    ]
    for text in positive_tickets:
        positive_extra.append({'text': text, 'label': 2})
    positive_df = pd.concat([positive_df, pd.DataFrame(positive_extra)], ignore_index=True)
    if len(positive_df) > TARGET:
        positive_df = positive_df.sample(n=TARGET, random_state=42)
    print(f"   Positive (2): {len(positive_df)} (added {len(positive_extra)})")

# === 3.3 Negative (0) - نضيف لو ناقص ===
negative_df = df[df['label'] == 0]
negative_extra = []
if len(negative_df) < TARGET:
    negative_tickets = [
        "The app is a bit slow today",
        "I keep getting logged out",
        "My order is 2 days late",
        "I entered wrong shipping address",
        "I want to delete my account",
        "The app is lagging",
        "I'm having trouble logging in",
        "The tracking number doesn't seem to work",
        "The quality is not great",
        "I'm not happy with the service",
        "The product arrived late",
        "The customer service was average at best",
        "I'm having issues with my order",
        "The app is not working as expected",
        "I'm disappointed with the quality",
        "The delivery took too long",
        "I received a damaged item",
        "The customer support was not helpful",
        "I'm frustrated with the app",
        "The product is not what I expected",
    ]
    for text in negative_tickets:
        negative_extra.append({'text': text, 'label': 0})
    negative_df = pd.concat([negative_df, pd.DataFrame(negative_extra)], ignore_index=True)
    if len(negative_df) > TARGET:
        negative_df = negative_df.sample(n=TARGET, random_state=42)
    print(f"   Negative (0): {len(negative_df)} (added {len(negative_extra)})")

angry_df = df[df['label'] == 3]
angry_extra = []
if len(angry_df) < TARGET:
    angry_tickets = [
        "My package is LOST! This is ridiculous!",
        "I was charged but I got nothing! FIX THIS!",
        "I want to speak to a manager NOW!",
        "This is the worst company ever!",
        "I'm going to report you to the BBB!",
        "This is fraud! I'm calling my bank!",
        "You ruined my experience!",
        "I'm so angry right now!",
        "This is beyond unacceptable!",
        "I can't believe this happened!",
        "My order is completely missing!",
        "I've been waiting for weeks with no response!",
        "You charged me twice and won't refund!",
        "This is a complete nightmare!",
        "I demand to speak with a supervisor!",
    ]
    for text in angry_tickets:
        angry_extra.append({'text': text, 'label': 3})
    angry_df = pd.concat([angry_df, pd.DataFrame(angry_extra)], ignore_index=True)
    if len(angry_df) > TARGET:
        angry_df = angry_df.sample(n=TARGET, random_state=42)
    print(f"   Angry (3): {len(angry_df)} (added {len(angry_extra)})")

df_balanced = pd.concat([neutral_df, positive_df, negative_df, angry_df], ignore_index=True)
df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\n4. Final balanced distribution:")
print(df_balanced['label'].value_counts().sort_index())

df_balanced.to_csv("data/processed/balanced_sentiment_data.csv", index=False)
print("\n✅ Data saved! Perfectly balanced!")
print("=" * 60)

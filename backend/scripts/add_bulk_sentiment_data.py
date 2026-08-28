# scripts/add_bulk_sentiment_data.py

import pandas as pd
import random

print("=" * 60)
print("📊 ADDING BULK SENTIMENT DATA")
print("=" * 60)


df = pd.read_csv("data/processed/balanced_sentiment_data.csv")
df = df.dropna()
print(f"\n1. Current data: {len(df)} samples")


new_data = []

neutral_tickets = [
    # Subscription & Billing
    "When does my subscription renew?",
    "How to change payment method?",
    "How long does refund take?",
    "Need to update billing address",
    "Where are account settings?",
    "How to turn off notifications?",
    "How to make profile private?",
    "New feature suggestion",
    "Does it work on Safari?",
    "Shipping options available",
    "Can I change my plan?",
    "How to view my invoice?",
    "How to download my data?",
    "What are the system requirements?",
    "How to enable dark mode?",
    "Is there a mobile app?",
    "How to invite team members?",
    "What are user roles?",
    "How to change my username?",
    "How to update my profile picture?",
    "How to set up email notifications?",
    "What is your privacy policy?",
    "How to contact support?",
    "What are support hours?",
    "Where can I find documentation?",
    "How to provide feedback?",
    "Can I export my data?",
    "How to schedule a demo?",
    "What integrations are available?",
    "How to use the search feature?",
    "How to filter results?",
    "What is the dashboard?",
    "How to customize my view?",
    "How to save my preferences?",
    "What are keyboard shortcuts?",
    "How to print my order?",
    "How to share my order?",
    "How to review my order?",
    "How to leave a review?",
    "How to rate your service?",
]

positive_tickets = [
    "I absolutely love your app! It's amazing!",
    "Great service, very helpful support team!",
    "Amazing experience, will definitely recommend!",
    "The new feature is wonderful, thank you!",
    "Best customer service I've ever had!",
    "I'm so impressed with your product!",
    "Thank you for your quick response!",
    "The support team was incredibly helpful!",
    "This is exactly what I needed, thank you!",
    "I'm so happy with the result!",
    "Your app has changed my life!",
    "I can't believe how easy this is!",
    "This is the best tool I've ever used!",
    "I'm so grateful for your help!",
    "The quality of your service is outstanding!",
    "I'm really impressed with the quality!",
    "Thank you for resolving my issue so quickly!",
    "Your team is fantastic, keep up the great work!",
    "I'm so glad I found your product!",
    "This is absolutely brilliant!",
    "I'm extremely satisfied with my experience!",
    "Your customer service is top-notch!",
    "I'm thrilled with how this turned out!",
    "The best decision I ever made!",
    "I'm blown away by the quality!",
    "This is a game-changer for me!",
    "I couldn't be happier with the service!",
    "Your attention to detail is amazing!",
    "I'm so glad I chose your company!",
    "This is perfect, exactly what I wanted!"
    "The new feature works exactly as expected",
    "My issue was resolved quickly and professionally", 
    "I'm really happy with the outcome",
    "The team went above and beyond to help me",
    "This is a huge improvement over the old version",
    "I'm very satisfied with the service",
    "The support team was knowledgeable and friendly",
    "Everything worked perfectly from start to finish",
    "I'm impressed by how fast you fixed the issue",
    "This is the best experience I've had with any company",
    "The product exceeded my expectations",
    "I'm grateful for your quick response",
    "You guys are doing an amazing job",
    "I will definitely be a loyal customer",
    "The solution you provided was perfect"
]

negative_tickets = [
    "The app keeps crashing and it's really frustrating",
    "I'm having trouble with my order",
    "The quality of the product is disappointing",
    "I've been waiting for a response for days",
    "The app is not working properly",
    "I'm unhappy with the service I received",
    "The delivery was very late",
    "I received the wrong item",
    "The customer support was not helpful",
    "I had a bad experience with your company",
    "The product arrived damaged",
    "I'm dissatisfied with the quality",
    "The app is slow and unresponsive",
    "I've had issues with my account",
    "The payment didn't go through",
    "I'm having trouble with the checkout process",
    "The product is not what I expected",
    "I'm disappointed with the purchase",
    "The return process is too complicated",
    "I didn't receive my order confirmation",
    "The tracking number doesn't work",
    "I'm having trouble logging in",
    "The app is not user-friendly",
    "I'm frustrated with the support team",
    "The product quality is poor",
    "I've been overcharged",
    "The shipping was too expensive",
    "I'm not satisfied with my purchase",
    "The customer service is terrible",
    "I would not recommend your product",
]

angry_tickets = [
    "I was charged twice! This is unacceptable!",
    "URGENT! Payment gateway is down!",
    "My card was billed twice! Need immediate refund!",
    "This is critical, fix it now!",
    "I demand a refund immediately!",
    "This is outrageous, I want my money back!",
    "I've been waiting for weeks, this is ridiculous!",
    "Nobody is responding to my tickets!",
    "This is the worst experience I've ever had!",
    "I'm furious about this situation!",
    "This is completely unacceptable!",
    "I need this fixed right now!",
    "This is a disaster!",
    "I'm absolutely furious about this!",
    "This is the worst customer service!",
    "I will never use your product again!",
    "This is a complete waste of time!",
    "I'm outraged by this experience!",
    "This is appalling service!",
    "I'm livid about this situation!",
]


for text in neutral_tickets:
    new_data.append((text, 1))

for text in positive_tickets:
    new_data.append((text, 2))

for text in negative_tickets:
    new_data.append((text, 0))

for text in angry_tickets:
    new_data.append((text, 3))


new_df = pd.DataFrame(new_data, columns=['text', 'label'])
df = pd.concat([df, new_df], ignore_index=True)

print(f"\n2. Added {len(new_data)} new samples")
print(f"   Total: {len(df)} samples")

print("\n3. New distribution:")
print(df['label'].value_counts().sort_index())


df.to_csv("data/processed/balanced_sentiment_data.csv", index=False)
print("\n✅ Data saved!")
print("=" * 60)
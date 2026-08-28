# scripts/build_faq.py


import sys
import os
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Force UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

import pandas as pd
import numpy as np
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("📚 BUILDING FAQ DATABASE (262 FAQ - FINAL)")
print("=" * 60)

# ============================================
# 1. تحميل FAQ الموجودة
# ============================================
print("\n1. Loading existing FAQs...")

existing_faq = None

possible_files = [
    './data/faq_combined.csv',
    'data/faq_combined.csv',
    '../data/faq_combined.csv'
]

for f in possible_files:
    if os.path.exists(f):
        existing_faq = pd.read_csv(f)
        print(f"   ✅ Loaded {len(existing_faq)} existing FAQs from {f}")
        break

if existing_faq is None:
    print("   ⚠️ No existing FAQ found")
    existing_faq = pd.DataFrame()

# ============================================
# 2. إضافة جميع الـ FAQs (262 FAQ)
# ============================================
print("\n2. Adding all FAQs (E-Commerce 100 + SaaS 100 + New 62)...")

all_faqs_list = [
    # ==========================================
    # E-COMMERCE / RETAIL (100 FAQ)
    # ==========================================
    {
        'question': 'How long does a refund take?',
        'answer': 'Refunds are processed within 3-5 business days after approval.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'I was charged twice. What should I do?',
        'answer': 'Contact support with your order number and both charge IDs.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I track my order?',
        'answer': 'Use the tracking link in your confirmation email or log in to your account.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why was my order cancelled?',
        'answer': 'Orders may be cancelled due to payment failure or stock issues.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I change my shipping address?',
        'answer': 'Contact support within 2 hours of placing the order.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I return an item?',
        'answer': 'Visit Returns Center in your account. Print return label.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your return policy?',
        'answer': '30-day return policy for unused items in original packaging.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How long does shipping take?',
        'answer': 'Standard: 3-5 business days. Express: 1-2 business days.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you offer free shipping?',
        'answer': 'Free shipping on orders over $50.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I cancel my order?',
        'answer': 'Yes, within 2 hours of placing the order.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I use a promo code?',
        'answer': 'Enter code at checkout in the Promo Code field.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why did my promo code not work?',
        'answer': 'Check expiry date and minimum purchase requirements.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I update my payment method?',
        'answer': 'Go to Account → Payment Methods → Add/Edit Card.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Is my payment secure?',
        'answer': 'Yes, we use industry-standard encryption (AES-256).',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What payment methods do you accept?',
        'answer': 'Credit/Debit Cards, PayPal, Apple Pay, Google Pay.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why was my payment declined?',
        'answer': 'Check card details, balance, or contact your bank.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I get an invoice?',
        'answer': 'Download invoice from Account → Orders → View Invoice.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I get a partial refund?',
        'answer': 'Partial refunds available for damaged or missing items.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your price match policy?',
        'answer': 'We price match competitors within 7 days of purchase.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you charge sales tax?',
        'answer': 'Sales tax applied based on your shipping address.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I reset my password?',
        'answer': "Click 'Forgot Password' on login page. Reset link emailed.",
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why is my account locked?',
        'answer': 'Locked after 5 failed login attempts. Contact support.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I delete my account?',
        'answer': 'Go to Settings → Account → Delete Account (permanent).',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I change my email?',
        'answer': 'Go to Settings → Account → Email → Update.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I enable 2FA?',
        'answer': 'Go to Settings → Security → Enable Two-Factor Authentication.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What are your support hours?',
        'answer': '24/7 via chat and email. Phone: Mon-Fri 9AM-6PM EST.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I contact support?',
        'answer': 'Chat, Email: support@company.com, Phone: +1-800-555-0199.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I provide feedback?',
        'answer': 'Use in-app feedback form or email feedback@company.com.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your privacy policy?',
        'answer': 'Available at company.com/privacy. We never sell your data.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Where can I find product documentation?',
        'answer': 'Available at docs.company.com.',
        'category': 'technical',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What browsers are supported?',
        'answer': 'Chrome, Firefox, Safari, Edge (latest 2 versions).',
        'category': 'technical',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I clear cache?',
        'answer': 'Chrome: Settings → Privacy → Clear browsing data.',
        'category': 'technical',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What to do if app crashes?',
        'answer': 'Update to latest version. Reinstall if persists.',
        'category': 'technical',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I report a bug?',
        'answer': 'Use in-app feedback or email support@company.com.',
        'category': 'technical',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How to check order status?',
        'answer': 'Login → Orders → Select Order → Track.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I change delivery date?',
        'answer': 'Contact support at least 24 hours before delivery.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What if package is damaged?',
        'answer': 'Take photos and contact support within 24 hours.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you ship internationally?',
        'answer': 'Yes, to over 50 countries. 7-14 business days.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What are international shipping fees?',
        'answer': 'Calculated at checkout based on destination.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I track international orders?',
        'answer': 'Yes, tracking available on all international orders.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I request a return label?',
        'answer': 'Print from Returns Center in your account.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What items are non-returnable?',
        'answer': 'Final sale items, perishable goods, and gift cards.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I exchange an item?',
        'answer': 'Start a return and place a new order.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I return a gift?',
        'answer': 'Yes, gift returns available with gift receipt.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How long does a refund take to appear?',
        'answer': '3-5 business days after processing.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I split payment?',
        'answer': 'Yes, split between two cards or card + gift card.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I use store credit?',
        'answer': 'Store credit applied automatically at checkout.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your subscription policy?',
        'answer': 'Cancel anytime. No hidden fees.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I change my plan?',
        'answer': 'Contact support to upgrade or downgrade your plan.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you offer discounts for students?',
        'answer': 'Yes, 10% student discount with valid ID.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your loyalty program?',
        'answer': 'Earn points on purchases. 100 points = $1.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I check my points?',
        'answer': 'Login → Account → Loyalty Points.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why are my points not showing?',
        'answer': 'Points appear after order completion (24 hours).',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I combine promo codes?',
        'answer': 'Only one promo code per order.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I unsubscribe from emails?',
        'answer': "Click 'Unsubscribe' at bottom of any email.",
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I update my profile?',
        'answer': 'Go to Account → Profile → Edit.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Why am I not receiving emails?',
        'answer': 'Check spam folder. Add us to contacts.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I change my phone number?',
        'answer': 'Go to Account → Profile → Phone Number.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your data retention policy?',
        'answer': 'Data retained for 7 years as required by law.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I request data deletion?',
        'answer': 'Submit request via Account → Privacy → Delete Data.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I have multiple accounts?',
        'answer': 'One account per user. Duplicate accounts may be merged.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I recover deleted account?',
        'answer': 'Contact support within 30 days of deletion.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your warranty policy?',
        'answer': '1-year warranty on all products.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I file a warranty claim?',
        'answer': 'Contact support with proof of purchase.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you have a physical store?',
        'answer': 'Online only. No physical retail locations.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I pick up my order?',
        'answer': 'No, online orders are shipped only.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What are your business hours?',
        'answer': '24/7 online. Phone support 9AM-6PM EST.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I find my order number?',
        'answer': 'Check confirmation email or login → Orders.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I add items to existing order?',
        'answer': 'No, new order required for additional items.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What if I enter wrong address?',
        'answer': 'Contact support immediately to correct.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you offer gift wrapping?',
        'answer': 'Yes, option available at checkout.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your shipping carrier?',
        'answer': 'USPS, FedEx, DHL depending on location.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I request signature confirmation?',
        'answer': 'Yes, option available at checkout.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I know if order shipped?',
        'answer': "You'll receive email confirmation with tracking.",
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What if I miss delivery?',
        'answer': 'Carrier will leave notice. Reschedule online.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I ship to a PO Box?',
        'answer': 'Yes, USPS shipping only for PO Boxes.',
        'category': 'delivery',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I file a complaint?',
        'answer': 'Email complaints@company.com or call support.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your response time?',
        'answer': 'Within 24 hours for emails. Instant for chat.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I escalate an issue?',
        'answer': 'Ask support agent to escalate to supervisor.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you have a community forum?',
        'answer': 'Yes, community.company.com.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I become an affiliate?',
        'answer': 'Yes, affiliate program available.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I apply for affiliate?',
        'answer': 'Visit company.com/affiliates.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your commission rate?',
        'answer': '10% of referred sales.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I withdraw affiliate earnings?',
        'answer': 'Via PayPal or bank transfer.',
        'category': 'general',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What happens if I forget password?',
        'answer': "Use 'Forgot Password' link to reset.",
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I enable guest checkout?',
        'answer': 'Checkout as guest without creating account.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I convert guest order to account?',
        'answer': 'Yes, contact support to link order.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What if I do not receive confirmation email?',
        'answer': 'Check spam. Request resend from account.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I change notification settings?',
        'answer': 'Account → Settings → Notifications.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I export my data?',
        'answer': 'Yes, account data export available on request.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I update my address?',
        'answer': 'Account → Address Book → Edit.',
        'category': 'account',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your fraud prevention?',
        'answer': 'We use advanced fraud detection and 3D Secure.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I dispute a charge?',
        'answer': 'Contact support with charge details.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your cancellation policy?',
        'answer': 'Cancel within 2 hours for full refund.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I get cashback?',
        'answer': 'Yes, cashback on eligible purchases.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I redeem cashback?',
        'answer': 'Cashback auto-applied to future orders.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What are your currency options?',
        'answer': 'Shop in USD, EUR, GBP, CAD, AUD.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How are exchange rates calculated?',
        'answer': 'Market rates + small processing fee.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Do you price adjust?',
        'answer': 'Yes, within 7 days of purchase.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'How do I apply for credit?',
        'answer': 'Store credit card available.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'What is your credit limit?',
        'answer': 'Based on credit approval.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },
    {
        'question': 'Can I use multiple currencies?',
        'answer': 'Order currency set at checkout.',
        'category': 'billing',
        'domain': 'E-Commerce / Retail'
    },

    # ==========================================
    # SAAS / TECH (100 FAQ)
    # ==========================================
    {
        'question': 'How do I reset my password?',
        'answer': "Use 'Forgot Password' on login page.",
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Why is my account suspended?',
        'answer': 'Check for unpaid invoices or violation of terms.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I upgrade my plan?',
        'answer': 'Go to Billing → Plans → Upgrade.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I cancel my subscription?',
        'answer': 'Go to Account → Subscriptions → Cancel.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Why was I charged after canceling?',
        'answer': 'If canceled after billing cycle, charge is valid.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I invite team members?',
        'answer': 'Go to Team → Invite → Enter email.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are the user roles?',
        'answer': 'Admin, Editor, Viewer.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I change user roles?',
        'answer': 'Team → Select User → Change Role.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I remove a team member?',
        'answer': 'Team → Select User → Remove.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your data security policy?',
        'answer': 'AES-256 encryption, TLS 1.3.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I integrate with Slack?',
        'answer': 'Integrations → Slack → Connect.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What APIs are available?',
        'answer': 'REST API, Webhooks, GraphQL.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I get API key?',
        'answer': 'Settings → API Keys → Generate.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are the rate limits?',
        'answer': 'Free: 100/min, Pro: 1000/min, Enterprise: Custom.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I export data?',
        'answer': 'Settings → Export → Choose Format.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What formats are supported?',
        'answer': 'CSV, JSON, XML.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I backup my data?',
        'answer': 'Automatic daily backups.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your uptime guarantee?',
        'answer': '99.9% uptime SLA.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I report an outage?',
        'answer': 'Status page or contact support.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I check system status?',
        'answer': 'status.company.com.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I change my email?',
        'answer': 'Settings → Account → Email.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I set up 2FA?',
        'answer': 'Security → Two-Factor Authentication → Enable.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your support hours?',
        'answer': '24/7 for critical issues.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I contact support?',
        'answer': 'Chat, Email: support@company.com.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I file a bug report?',
        'answer': 'Use in-app feedback or email.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I request a feature?',
        'answer': 'Feature Request portal or feedback form.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your feature release cycle?',
        'answer': 'Monthly releases.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I join beta program?',
        'answer': 'Settings → Beta → Join.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your pricing model?',
        'answer': 'Subscription-based, billed monthly/yearly.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Do you offer discounts?',
        'answer': 'Annual plans get 20% discount.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What payment methods?',
        'answer': 'Credit Card, PayPal, Invoice.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I pay by invoice?',
        'answer': 'Contact sales for invoice setup.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your refund policy?',
        'answer': '30-day money-back guarantee.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I pause subscription?',
        'answer': 'Yes, pause for up to 3 months.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I transfer subscription?',
        'answer': 'Contact support for ownership transfer.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your GDPR compliance?',
        'answer': 'Full GDPR compliant.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I request data deletion?',
        'answer': 'Account → Privacy → Delete Data.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I request data export?',
        'answer': 'Settings → Export → Request Data.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What data do you collect?',
        'answer': 'Email, name, usage data.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How long is data retained?',
        'answer': '7 years.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I update billing information?',
        'answer': 'Billing → Payment Methods → Update.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are your currency options?',
        'answer': 'USD, EUR, GBP, CAD.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I view invoices?',
        'answer': 'Billing → Invoices.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I download invoices?',
        'answer': 'Billing → Invoices → Download PDF.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What if payment fails?',
        'answer': 'Retry or update payment method.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I apply promo code?',
        'answer': 'Billing → Coupon → Enter Code.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your coupon policy?',
        'answer': 'One coupon per subscription.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I get a refund for unused time?',
        'answer': 'Pro-rated refunds available.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I change plan tier?',
        'answer': 'Billing → Plans → Select New Plan.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What happens on plan downgrade?',
        'answer': 'Data retained, features removed.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I add storage?',
        'answer': 'Billing → Storage → Add.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are storage limits?',
        'answer': 'Free: 10GB, Pro: 100GB, Enterprise: Custom.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I manage users?',
        'answer': 'Settings → Users → Manage.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are SSO options?',
        'answer': 'SAML, Google, Microsoft.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I set up SAML?',
        'answer': 'Security → SAML → Configure.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I backup data?',
        'answer': 'Automatic daily with point-in-time recovery.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I restore data?',
        'answer': 'Contact support for restoration.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What audit logs are available?',
        'answer': 'User login, settings changes, data exports.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I view audit logs?',
        'answer': 'Settings → Audit Logs.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I white-label the product?',
        'answer': 'Enterprise plan only.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I set up webhooks?',
        'answer': 'Settings → Webhooks → Add.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What webhook events are available?',
        'answer': 'user.created, subscription.updated, payment.failed.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I test webhooks?',
        'answer': 'Webhooks → Test → Send Test Event.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your API documentation?',
        'answer': 'docs.company.com/api.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I authenticate API requests?',
        'answer': 'API Key header: X-API-Key.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are API response formats?',
        'answer': 'JSON only.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I handle API errors?',
        'answer': 'Check error codes and retry.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your rate limit policy?',
        'answer': 'Exceed limit = 429 response.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I request rate limit increase?',
        'answer': 'Contact support for approval.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What compliance standards?',
        'answer': 'GDPR, SOC2, ISO 27001.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I report a security issue?',
        'answer': 'security@company.com.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are your business hours?',
        'answer': '24/7 critical support. Business hours 9-6 EST.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I schedule a demo?',
        'answer': 'Contact sales or book online.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I update payment method?',
        'answer': 'Billing → Payment Methods.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What if my account is hacked?',
        'answer': 'Immediate password reset and contact support.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I enable MFA?',
        'answer': 'Security → Multi-Factor Authentication.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are login session limits?',
        'answer': 'Sessions expire after 7 days.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I logout all devices?',
        'answer': 'Account → Security → Logout All.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I use custom domains?',
        'answer': 'Yes, Enterprise plan.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I set up custom domain?',
        'answer': 'Settings → Domains → Add.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I verify domain ownership?',
        'answer': 'Add TXT record to DNS.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are email delivery settings?',
        'answer': 'Configure from Settings → Email.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I test email delivery?',
        'answer': 'Settings → Email → Test Send.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I customize emails?',
        'answer': 'Settings → Email → Templates.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What integrations are available?',
        'answer': 'Slack, Teams, Zapier, Salesforce.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I connect Zapier?',
        'answer': 'Integrations → Zapier → Connect.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I export user list?',
        'answer': 'Settings → Export → Users CSV.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I import users?',
        'answer': 'Settings → Import → Upload CSV.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is the user import format?',
        'answer': 'CSV with email, name, role.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I send bulk emails?',
        'answer': 'Settings → Email → Bulk Send.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I manage notification preferences?',
        'answer': 'Settings → Notifications.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are default notification settings?',
        'answer': 'Email and in-app notifications.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I opt out of marketing emails?',
        'answer': 'Settings → Notifications → Unsubscribe.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your chatbot availability?',
        'answer': '24/7 for basic queries.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I escalate from chatbot?',
        'answer': 'Type "human" or "support agent".',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I access knowledge base?',
        'answer': 'help.company.com.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I submit knowledge base article?',
        'answer': 'Contact support with draft.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are your community guidelines?',
        'answer': 'Available at company.com/community.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I report inappropriate content?',
        'answer': 'Report button or email.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What is your referral program?',
        'answer': 'Refer friends, get $10 credit.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I redeem referral credit?',
        'answer': 'Applied automatically to next bill.',
        'category': 'general',
        'domain': 'SaaS / Tech'
    },

    # ==========================================
    # NEW FAQs (62 FAQ - من الملف السابق)
    # ==========================================
    {
        'question': 'How do I change my email?',
        'answer': 'Go to Settings → Account → Email. Enter new email and confirm via verification link sent to new address.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'Why is my account locked?',
        'answer': 'Accounts lock after multiple failed login attempts. Use "Forgot Password" to reset or wait 30 minutes.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'How do I enable 2FA?',
        'answer': 'Go to Settings → Security → 2FA. Scan QR code with authenticator app (Google Authenticator, Authy).',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'What are the password requirements?',
        'answer': 'Minimum 8 characters, include uppercase, lowercase, number, and special character.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'Account locked after multiple login attempts.',
        'answer': 'Security feature after 5 failed logins. Wait 30 minutes or use password reset to unlock immediately.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'Locked out by two-factor auth.',
        'answer': 'Contact support with account email and ID verification (e.g., last order details). We can disable 2FA after verifying.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'How to manage user groups?',
        'answer': 'Settings → Team → Groups → Create Group. Add users to groups, assign group-level permissions. Simplifies permission management for large teams.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to transfer workspace ownership?',
        'answer': 'Settings → Team → find user → Transfer Ownership. You\'ll be demoted to Admin. New owner receives confirmation email.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I transfer my account to someone else?',
        'answer': 'Accounts are non-transferable. New user must create their own account.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'Account showing wrong country/currency.',
        'answer': 'Set at account creation. Contact support to change — requires re-entering payment details due to currency conversion.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'How to set up multi-workspace access?',
        'answer': 'Users can be members of multiple workspaces. Switch between workspaces using workspace dropdown in top navigation. Each workspace has separate billing, data, settings.',
        'category': 'account',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I delete my account?',
        'answer': 'Go to Account → Settings → Delete Account. This action is permanent and removes all order history and points.',
        'category': 'account',
        'domain': 'General'
    },
    {
        'question': 'Why was I charged after canceling?',
        'answer': 'If you canceled after the billing cycle date, the charge is for the previous month. Contact support for clarification.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I update my payment method?',
        'answer': 'Go to Settings → Billing → Payment Methods. Add new card and set as default.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'Can I get a partial refund?',
        'answer': 'Partial refunds are available for unused subscription time or damaged items.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'What is your refund policy?',
        'answer': '30-day money-back guarantee for subscriptions and 14-day return for products.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'How do I get an invoice?',
        'answer': 'Download invoices from Settings → Billing → Invoices or from My Orders → select order → Download Invoice.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'How to get copy of past invoice?',
        'answer': 'Settings → Billing → Invoice History → select month → Download PDF. All invoices available from account creation date.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I get VAT invoice for business?',
        'answer': 'Go to My Orders → select order → Download VAT Invoice. If account not set up, contact support with VAT number.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'Can I get a receipt for tax purposes?',
        'answer': 'Invoices serve as receipts for tax. Download from My Orders or contact support for specific tax documentation.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'How does seat-based billing work?',
        'answer': "You're billed for number of active seats (user accounts) in workspace. Removing user deactivates seat. Billing adjusts start of next billing cycle.",
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I backdate a plan change?',
        'answer': 'Plan changes effective immediately or scheduled for next cycle. Cannot backdate to prior periods due to billing system limitations.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What happens if payment fails on annual plan?',
        'answer': 'You have 7 days to update payment method. If not resolved, workspace suspended. Annual commitment still applies — balance due upon reactivation.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to dispute billing charge?',
        'answer': 'Settings → Billing → Dispute Charge or contact support. Include invoice number and charge description. Disputes reviewed within 3 business days.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Why was I charged sales tax?',
        'answer': 'Sales tax applied based on billing address location where legally required. If tax-exempt, upload certificate in Settings → Billing → Tax Exemption.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What currencies supported for billing?',
        'answer': 'We support USD, EUR, GBP, CAD, AUD. Currency set at account creation. Contact support to change — requires re-entering payment details.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Why is my refund only partial?',
        'answer': 'Partial refunds occur when items lack original packaging or are damaged. Check return confirmation for breakdown.',
        'category': 'billing',
        'domain': 'General'
    },
    {
        'question': 'Can I change my plan?',
        'answer': 'Yes! Go to Settings → Billing → Change Plan. Upgrades apply immediately, downgrades at next billing cycle.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to downgrade plan?',
        'answer': 'Settings → Billing → Change Plan → select lower plan. Downgrades effective end of current billing period. No charge for unused time.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How does annual plan discount work?',
        'answer': 'Annual plans billed upfront for 12 months at 20% discount versus monthly rate. Discount applied automatically at checkout when selecting annual billing.',
        'category': 'billing',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How long does delivery take?',
        'answer': 'Standard: 3-5 business days. Express: 1-2 business days.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Do you ship internationally?',
        'answer': 'Yes, to over 50 countries. Takes 7-14 business days.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'How do I track my order?',
        'answer': 'Track from confirmation email or login to your account → My Orders → Track.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'What if my package is lost?',
        'answer': 'Contact support within 30 days for investigation and replacement/refund.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Can I change delivery address?',
        'answer': 'Change before shipment by contacting support. After shipment, use tracking link to redirect.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'How to track international order?',
        'answer': 'International tracking on Track Package page. Customs processing can add 3–10 business days.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Tracking hasn\'t updated in 5 days. Is package lost?',
        'answer': 'Gaps occur at sorting facilities. If no update after 7 business days, contact support for carrier investigation.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Order arrived damaged. What now?',
        'answer': 'Don\'t discard packaging. Take photos and contact support within 48 hours for replacement or refund.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Package says delivered but I didn\'t get it.',
        'answer': 'Check with neighbours and safe locations. If not found, contact support within 7 days to file claim.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'My order is late. What to do?',
        'answer': 'Check tracking first. If no update for 3+ business days, contact support with order number.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'Can I redirect package in transit?',
        'answer': 'Use tracking link to access carrier\'s redirect options (hold at location, neighbor delivery, etc).',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'What if I\'m not home when order arrives?',
        'answer': 'Carrier leaves package in safe location if possible, or collection notice. Redirect to pickup via tracking link.',
        'category': 'delivery',
        'domain': 'General'
    },
    {
        'question': 'How do I report a bug?',
        'answer': 'Report bugs via the in-app feedback form or email support@company.com with steps to reproduce.',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'What browsers are supported?',
        'answer': 'Chrome, Firefox, Safari, and Edge (latest 2 versions).',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'What is the system status?',
        'answer': 'Check status.company.com for real-time updates.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How do I clear cache?',
        'answer': 'Chrome: Settings → Privacy → Clear browsing data. Firefox: Settings → Privacy & Security → Clear Data.',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'What are the API rate limits?',
        'answer': 'Free: 100/min. Pro: 1000/min. Enterprise: Custom. Check X-RateLimit headers in API responses.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to troubleshoot API errors?',
        'answer': 'Check API error response for error code and message. Common codes: 400 (bad request), 401 (unauthorized), 404 (not found), 429 (rate limit), 500 (server error).',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Webhook not receiving events. How to debug?',
        'answer': 'Check webhook delivery logs in Settings → Developer → Webhooks → select endpoint → View Logs. Common issues: endpoint returning non-200 status or incorrect HTTPS configuration.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to generate and rotate API keys?',
        'answer': 'Settings → Developer → API Keys. Click key name to view options including Rotate (generates new key, old stays valid 24 hours) and Revoke.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to get API key?',
        'answer': 'Settings → Developer → API Keys → Create New Key. Store securely — shown only once. If lost, revoke and regenerate.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to export all workspace data?',
        'answer': 'Settings → Data → Export → select data types → Start Export. Download link emailed when ready (typically within 1 hour for workspaces under 10GB).',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'How to migrate data from another platform?',
        'answer': 'We provide migration tools for common platforms. Settings → Data → Migrate. For custom migrations, our solutions team offers assisted migration services.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Can I export data from dashboard?',
        'answer': 'Yes! Go to Dashboard → Export → Select data range → Download CSV or Excel.',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'Is there a dark mode feature?',
        'answer': 'Dark mode is available in Settings → Appearance → Theme → Dark. Or use system default setting.',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'Dashboard loading very slowly.',
        'answer': 'Slow dashboards often caused by large date ranges or many filters. Try narrowing date range. If persists across browsers and networks, contact support.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'Website very slow today. Is there outage?',
        'answer': 'Check status.company.com for real-time platform updates. If no outage listed and continues, contact support.',
        'category': 'technical',
        'domain': 'General'
    },
    {
        'question': 'Where is the documentation?',
        'answer': 'Available at docs.company.com.',
        'category': 'technical',
        'domain': 'SaaS / Tech'
    },
    {
        'question': 'What are support hours?',
        'answer': '24/7 chat and email. Phone: Mon-Fri 9AM-6PM EST.',
        'category': 'general',
        'domain': 'General'
    },
    {
        'question': 'How to contact support?',
        'answer': 'Chat, Email: support@company.com, Phone: +1-800-555-0199.',
        'category': 'general',
        'domain': 'General'
    },
    {
        'question': 'How to provide feedback?',
        'answer': 'In-app feedback form or email feedback@company.com.',
        'category': 'general',
        'domain': 'General'
    },
    {
        'question': 'What is the privacy policy?',
        'answer': 'Available at company.com/privacy.',
        'category': 'general',
        'domain': 'General'
    },
]

print(f"   ✅ Total FAQs in list: {len(all_faqs_list)}")

# ============================================
# 3. دمج الكل
# ============================================
print("\n3. Merging all FAQs...")

# دمج الـ FAQs الجديدة مع الـ existing (لو موجود)
if len(existing_faq) > 0:
    all_faqs = pd.concat([existing_faq, pd.DataFrame(all_faqs_list)], ignore_index=True)
    all_faqs = all_faqs.drop_duplicates(subset=['question'], keep='first')
    print(f"   ✅ Merged {len(all_faqs)} unique FAQs (existing + new)")
else:
    all_faqs = pd.DataFrame(all_faqs_list)
    print(f"   ✅ {len(all_faqs)} FAQs ready")

# ============================================
# 4. توليد Embeddings وبناء FAISS
# ============================================
print("\n4. Generating embeddings...")

try:
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    print("   ✅ Model loaded successfully")
except Exception as e:
    print(f"   ⚠️ Error loading model: {e}")
    print("   Trying fallback model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

# توليد النصوص
all_faqs['text'] = all_faqs['question'] + " " + all_faqs['answer']
faq_texts = all_faqs['text'].tolist()

print(f"   Generating embeddings for {len(faq_texts)} FAQs...")

# توليد Embeddings
faq_embeddings = model.encode(
    faq_texts,
    batch_size=32,
    normalize_embeddings=True,
    show_progress_bar=True
)

print(f"   ✅ Embeddings shape: {faq_embeddings.shape}")

# ============================================
# 5. بناء FAISS Index
# ============================================
print("\n5. Building FAISS index...")

dimension = faq_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(faq_embeddings.astype('float32'))

print(f"   ✅ FAISS index created with {index.ntotal} vectors")

# ============================================
# 6. حفظ الملفات
# ============================================
print("\n6. Saving files...")

os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# حفظ FAISS index
faiss.write_index(index, 'models/faq_index.faiss')
faiss.write_index(index, 'models/faq_index_optimized.faiss')
print("   ✅ Saved: models/faq_index.faiss")
print("   ✅ Saved: models/faq_index_optimized.faiss")

# حفظ Metadata
metadata = all_faqs[['question', 'answer', 'category', 'domain']].to_dict('records')
with open('models/faq_metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)
print("   ✅ Saved: models/faq_metadata.pkl")

# حفظ البيانات كاملة
all_faqs.to_csv('data/faq_combined.csv', index=False)
print("   ✅ Saved: data/faq_combined.csv")

# ============================================
# 7. SUMMARY
# ============================================
print("\n" + "="*60)
print("📊 FAQ BUILD SUMMARY")
print("="*60)
print(f"   Total FAQs: {len(all_faqs)}")
print(f"   Categories: {all_faqs['category'].unique().tolist()}")
print(f"   Domains: {all_faqs['domain'].unique().tolist()}")

print("\n📋 Category Distribution:")
print(all_faqs['category'].value_counts().to_string())

print("\n" + "="*60)
print("✅ FAQ DATABASE BUILT SUCCESSFULLY!")
print("="*60)
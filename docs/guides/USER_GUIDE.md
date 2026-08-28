# 👤 User Guide — Customer Support AI

> Simple, step-by-step guide for end users using the Customer Support AI system.

---

## 📋 Table of Contents

* [What is Customer Support AI?](#what-is-customer-support-ai)
* [Getting Started](#getting-started)

  * [Creating an Account](#creating-an-account)
  * [Logging In](#logging-in)
* [Using the Dashboard](#using-the-dashboard)

  * [Main Dashboard](#main-dashboard)
  * [Submitting a Ticket](#submitting-a-ticket)
  * [Understanding Results](#understanding-results)
* [Viewing Ticket History](#viewing-ticket-history)
* [Admin Dashboard](#admin-dashboard)

  * [Accessing the Admin Dashboard](#accessing-the-admin-dashboard)
  * [Dashboard Features](#dashboard-features)
* [FAQ](#faq)

  * [General Questions](#general-questions)
  * [Technical Questions](#technical-questions)
* [Troubleshooting](#troubleshooting)
* [Support](#support)
* [Quick Reference](#quick-reference)

---

# 🤖 What is Customer Support AI?

Customer Support AI is an intelligent customer support system that automatically analyzes submitted support tickets and provides useful insights and relevant solutions.

The system analyzes each ticket using multiple AI components:

* **Category Classification** — Identifies the type of issue.
* **Priority Prediction** — Estimates how urgent the issue is.
* **Sentiment Analysis** — Determines the customer's emotional state.
* **Smart Solutions** — Retrieves relevant answers from the FAQ knowledge base.
* **Ticket History** — Keeps track of previously submitted tickets.

---

## ✨ Key Benefits

| Benefit                   | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| ⚡ **Speed**               | Receive ticket analysis within seconds.                     |
| 🎯 **Automated Analysis** | Automatically classify and evaluate support requests.       |
| 📊 **Insights**           | Understand ticket priority and customer sentiment.          |
| 🔍 **Smart Search**       | Retrieve relevant solutions from the FAQ database.          |
| 📈 **Tracking**           | Review previously submitted tickets through ticket history. |

---

# 🚀 Getting Started

## Creating an Account

### Step 1 — Open the Application

For local development, open:

```text
http://localhost:3000
```

> The URL may be different when the application is deployed to another environment.

---

### Step 2 — Open the Sign-Up Page

Click:

**Sign Up**

---

### Step 3 — Enter Your Information

Provide the required information:

* Full Name
* Email Address
* Password

---

### Step 4 — Create Your Account

Click:

**Get Started**

---

### Step 5 — Verify Your Email

If email verification is enabled, check your inbox and follow the verification instructions.

---

## Logging In

To access your account:

1. Open the application.
2. Click **Sign In**.
3. Enter your email address.
4. Enter your password.
5. Click **Sign In**.
6. You will be redirected to your dashboard.

---

# 📊 Using the Dashboard

## Main Dashboard

After logging in, the dashboard provides access to the main features of the system.

Typical dashboard sections include:

1. **User Information** — Displays your account information.
2. **Ticket Form** — Submit a new support ticket.
3. **Navigation** — Access Dashboard, History, and Logout.
4. **Analysis Results** — View the AI-generated ticket analysis.

---

## Submitting a Ticket

### Step 1 — Enter Ticket Information

Complete the ticket form.

| Field               | Description                              | Example                                         |
| ------------------- | ---------------------------------------- | ----------------------------------------------- |
| **Title**           | Short summary of the issue               | `Payment was charged twice`                     |
| **Description**     | Detailed explanation of the issue        | `My card was charged twice for the same order.` |
| **Resolution Time** | Estimated resolution time, if applicable | `4` hours                                       |

Provide as much relevant information as possible in the title and description.

---

### Step 2 — Analyze the Ticket

After completing the form, click:

**Analyze Ticket**

The system will process the ticket and generate its predictions.

---

### Step 3 — Review the Results

The analysis result may include:

```text
┌──────────────────────────────────────────────────────────────┐
│                    Ticket Analysis Results                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  📂 Category: billing                                        │
│                                                              │
│  🚀 Priority: High                                           │
│     Confidence: 61.2%                                        │
│                                                              │
│  😡 Sentiment: angry                                         │
│                                                              │
│  💡 Suggested Solution:                                      │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Contact support with your order number. Refunds        │  │
│  │ are processed within 3–5 business days.               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  📚 Source: FAQ                                              │
│     Confidence: 75.5%                                        │
│                                                              │
│  🔍 Related FAQs:                                            │
│     • I was charged twice. What should I do? — 72.1%       │
│     • How long does a refund take? — 68.3%                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

# 📌 Understanding Results

## 1. Category

The category indicates the general type of problem identified by the AI.

| Category      | Meaning                                 | Example                      |
| ------------- | --------------------------------------- | ---------------------------- |
| **technical** | Technical or application-related issues | `App crashes on startup`     |
| **billing**   | Payment, invoice, or charging issues    | `I was charged twice`        |
| **account**   | Account, login, or profile issues       | `I cannot reset my password` |
| **delivery**  | Shipping and order delivery issues      | `My package never arrived`   |

---

## 2. Priority

Priority indicates how urgently the ticket should be handled.

| Priority   | Meaning                                | Recommended Response                          |
| ---------- | -------------------------------------- | --------------------------------------------- |
| **High**   | Urgent or critical issue               | Respond as soon as possible                   |
| **Medium** | Important but not immediately critical | Respond within the normal support workflow    |
| **Low**    | Non-critical issue                     | Can be handled after higher-priority requests |

> Priority predictions are AI-generated recommendations and should be reviewed according to your organization's support policies.

---

## 3. Sentiment

Sentiment describes the emotional tone detected in the customer's message.

| Sentiment       | Meaning                                                 |
| --------------- | ------------------------------------------------------- |
| 😊 **positive** | Customer appears satisfied or happy                     |
| 😐 **neutral**  | Customer appears neither strongly positive nor negative |
| 😠 **negative** | Customer appears frustrated or dissatisfied             |
| 😡 **angry**    | Customer appears strongly upset or angry                |

---

## 4. Suggested Solution

The system uses the FAQ knowledge base to retrieve a relevant solution.

If a sufficiently relevant FAQ is found, the system may display:

* Suggested answer.
* FAQ source.
* Retrieval confidence.
* Related FAQ entries.

If no suitable FAQ is available, the system may provide a general response instead.

---

## 5. Confidence Scores

A confidence score indicates how strongly the model or retrieval system supports a prediction.

For example:

```text
Priority Confidence: 61.2%
FAQ Confidence:      75.5%
```

A higher score generally indicates stronger model or retrieval confidence.

> Confidence scores should be interpreted as model signals rather than guaranteed probabilities of correctness.

---

# 📜 Viewing Ticket History

## Accessing History

To view previously submitted tickets:

1. Open the application.
2. Sign in to your account.
3. Click **My History** in the navigation bar.

---

## History Features

| Feature             | Description                                                              |
| ------------------- | ------------------------------------------------------------------------ |
| 🔍 **Search**       | Search tickets by title or description.                                  |
| 🎯 **Filter**       | Filter tickets by priority or category.                                  |
| 📊 **Statistics**   | View summary statistics such as total tickets and high-priority tickets. |
| 📋 **Ticket Table** | View ticket information in an organized table.                           |

---

## History Table

The history page may contain the following columns:

| Column        | Description                 |
| ------------- | --------------------------- |
| **#**         | Ticket number or identifier |
| **Title**     | Ticket title                |
| **Category**  | Predicted category          |
| **Priority**  | Predicted priority          |
| **Sentiment** | Predicted sentiment         |
| **Source**    | FAQ or General              |
| **Date**      | Ticket submission date      |

---

# 👑 Admin Dashboard

> **Access:** The Admin Dashboard is available only to authorized users with the required administrator permissions.

## Accessing the Admin Dashboard

Depending on the application configuration:

1. Sign in with an authorized account.
2. Open the **Dashboard** or admin section.
3. Enter the required administrator key if prompted.

---

## Dashboard Features

### 1. Metrics Cards

The dashboard can provide high-level system statistics.

| Metric                    | Description                                   |
| ------------------------- | --------------------------------------------- |
| 📥 **Total Predictions**  | Total number of ticket predictions processed. |
| ⏱️ **Uptime**             | Amount of time the system has been running.   |
| 🎯 **Average Confidence** | Average confidence across predictions.        |
| ❌ **Errors**              | Number of recorded system errors.             |

---

### 2. Charts

The admin dashboard may display:

* **Priority Distribution** — Breakdown of High, Medium, and Low tickets.
* **Sentiment Distribution** — Distribution across sentiment classes.
* **Source Distribution** — FAQ versus General responses.

---

### 3. Performance Overview

Performance metrics may include:

* **Priority Confidence** — Average confidence of priority predictions.
* **RAG Confidence** — Average confidence of FAQ retrieval.

---

### 4. Export Data

To export prediction data:

1. Open the Admin Dashboard.
2. Locate the **Export CSV** option.
3. Click **Export CSV**.
4. Save the generated CSV file.

---

# ❓ FAQ

## General Questions

### Q: How accurate is the system?

A: The system uses trained machine learning models to classify ticket category, priority, and sentiment. Model accuracy can vary depending on the task and dataset used for training and evaluation.

### Q: What happens if no FAQ matches my question?

A: If no sufficiently relevant FAQ is found, the system can provide a general response and recommend contacting support.

### Q: Can I see my previous tickets?

A: Yes. Open **My History** to view previously submitted tickets and their analysis results.

### Q: Is my data secure?

A: The application is designed with authentication and secure password handling. Production deployments should also use secure environment variables, HTTPS, access controls, and appropriate data-protection practices.

---

## Technical Questions

### Q: Why was my ticket classified as `technical`?

A: The classification model analyzes the text of your ticket and identifies patterns associated with technical issues, such as application errors, crashes, synchronization problems, or other technical terms.

### Q: What does RAG Confidence mean?

A: RAG Confidence represents how strongly the retrieval system considers a particular FAQ relevant to your ticket.

A higher retrieval confidence generally means that the FAQ is more semantically similar to the submitted request.

### Q: Can I update a ticket after submitting it?

A: Tickets are currently treated as read-only after submission. If additional information is needed, submit a new ticket with the updated details.

---

# 🔧 Troubleshooting

## Login Issues

### Problem

You receive an:

```text
Invalid credentials
```

error.

### Solution

Try the following:

1. Verify your email address.
2. Verify your password.
3. Check whether Caps Lock is enabled.
4. Use **Forgot Password** if the feature is available.
5. Contact an administrator or support representative if you remain locked out.

---

## Ticket Submission Issues

### Problem

The ticket cannot be submitted.

### Solution

1. Check your internet connection.
2. Verify that all required fields are completed.
3. Make sure the ticket description contains valid text.
4. Try refreshing the page.
5. Sign in again if your session has expired.
6. Contact support if the issue continues.

---

## Results Not Showing

### Problem

No analysis results appear after submitting a ticket.

### Solution

1. Wait a few seconds while the system processes the request.
2. Check whether the backend service is available.
3. Refresh the page if necessary.
4. If you have administrator access, verify that the required ML models are loaded.
5. Contact support if the problem persists.

---

## Slow Performance

### Problem

The application is responding slowly.

### Solution

Try the following:

1. Check your internet connection.
2. Refresh the application.
3. Close unnecessary browser tabs.
4. Try another browser if the problem continues.
5. Contact support if the issue persists.

---

# 📞 Support

## Getting Help

For assistance, use the support channels provided by your deployment.

Possible support options include:

* **Email Support**
* **Live Chat**
* **In-App Feedback**
* **Knowledge Base**
* **GitHub Issues** for development-related problems

For the project repository:

```text
https://github.com/Aya-Mohamed945/customer-support-ai
```

---

## Feedback

Your feedback helps improve the system.

You can provide feedback through:

* In-app feedback functionality.
* The project's designated support channel.
* GitHub Issues for technical or development-related issues.

When reporting a technical issue, include:

* A short description of the problem.
* The steps that caused the issue.
* Any displayed error message.
* The affected page or feature.
* Screenshots when useful.

---

# 🎯 Quick Reference

## Dashboard Navigation

```text
┌─────────────────────────────────────────────────────────────┐
│  [Logo] Customer Support AI                                 │
│                                                             │
│  👤 User       📊 Dashboard       📜 History       🚪 Logout │
└─────────────────────────────────────────────────────────────┘
```

---

## Ticket Form

```text
┌─────────────────────────────────────────────────────────────┐
│                       📝 New Ticket                         │
│                                                             │
│  Title:                                                     │
│  [_____________________________________________________]    │
│                                                             │
│  Description:                                               │
│  [_____________________________________________________]    │
│  [_____________________________________________________]    │
│  [_____________________________________________________]    │
│                                                             │
│  Resolution Time: [________] hours                          │
│                                                             │
│                   [ 🔍 Analyze Ticket ]                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Analysis Results

| Icon | Meaning            |
| ---- | ------------------ |
| 📂   | Category           |
| 🚀   | Priority           |
| 😊   | Sentiment          |
| 💡   | Suggested Solution |
| 📚   | FAQ Source         |
| 🔍   | Related FAQs       |

---

## Typical User Workflow

```text
Create Account
      │
      ▼
   Sign In
      │
      ▼
   Dashboard
      │
      ▼
Submit Ticket
      │
      ▼
 AI Analysis
      │
      ├───────────────┐
      ▼               ▼
  Predictions     FAQ Retrieval
      │               │
      └───────┬───────┘
              ▼
       View Results
              │
              ▼
        Ticket History
```

---

<div align="center">

<strong>Customer Support AI — User Guide</strong>

<br>

Last Updated: August 2026

</div>

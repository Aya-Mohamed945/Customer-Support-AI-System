# test_api.py
"""
🧪 Test API with RAG Integration
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("🧪 TESTING HEALTH ENDPOINT")
    print("="*60)
    
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   ✅ Status: {r.status_code}")
        print(f"   ✅ Response: {json.dumps(r.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_rag():
    """Test RAG endpoint"""
    print("\n" + "="*60)
    print("🧪 TESTING RAG ENDPOINT")
    print("="*60)
    
    test_queries = [
        "How long does a refund take?",
        "I was charged twice, what should I do?",
        "How do I reset my password?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        try:
            r = requests.post(
                f"{BASE_URL}/api/v1/rag/retrieve",
                json={"query": query, "k": 2, "threshold": 0.3},
                timeout=10
            )
            
            if r.status_code == 200:
                results = r.json().get('results', [])
                print(f"   ✅ Found {len(results)} results")
                for i, res in enumerate(results, 1):
                    print(f"      {i}. {res.get('question', '')[:60]}... (similarity: {res.get('similarity', 0):.3f})")
                    if res.get('answer'):
                        print(f"         Answer: {res.get('answer', '')[:80]}...")
            else:
                print(f"   ❌ Error: {r.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_prediction_with_rag():
    """Test prediction with RAG"""
    print("\n" + "="*60)
    print("🧪 TESTING PREDICTION WITH RAG")
    print("="*60)
    
    test_cases = [
        {
            "title": "Payment was charged twice",
            "description": "My card was charged twice for the same order. Need refund immediately.",
            "resolution_time": 2
        },
        {
            "title": "How long does refund take",
            "description": "I requested a refund 5 days ago and haven't received it yet.",
            "resolution_time": 120
        }
    ]
    
    for data in test_cases:
        print(f"\n📝 Title: {data['title']}")
        print(f"   Description: {data['description'][:60]}...")
        
        try:
            r = requests.post(f"{BASE_URL}/api/v1/predict", json=data, timeout=30)
            
            if r.status_code == 200:
                result = r.json()
                print(f"   ✅ Priority: {result.get('priority')} (Confidence: {result.get('priority_confidence'):.3f})")
                print(f"   ✅ Category: {result.get('category')}")
                print(f"   ✅ Sentiment: {result.get('sentiment')}")
                print(f"\n   💡 Suggested Solution:")
                print(f"      {result.get('suggested_solution', '')[:150]}...")
                print(f"   📚 Source: {result.get('source')} (Confidence: {result.get('rag_confidence', 0):.3f})")
                
                if result.get('rag_results'):
                    print(f"\n   📚 FAQ Results:")
                    for res in result['rag_results']:
                        print(f"      - {res.get('question', '')} (Similarity: {res.get('similarity', 0):.3f})")
            else:
                print(f"   ❌ Error: {r.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 TESTING CUSTOMER SUPPORT AI API WITH RAG")
    print("="*60)
    
    if test_health():
        test_rag()
        test_prediction_with_rag()
    
    print("\n" + "="*60)
    print("✅ TESTING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
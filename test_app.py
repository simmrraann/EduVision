#!/usr/bin/env python3
"""
Test script for MindMorph application
"""

import requests
import json
import time

def test_app():
    """Test the MindMorph application endpoints"""
    
    base_url = "http://localhost:5000"
    
    print("🧠 Testing MindMorph Application...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Server is running successfully")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the application with: python app.py")
        return
    
    # Test 2: Test feature generation endpoints
    test_text = "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions or decisions based on that data."
    
    endpoints = [
        ("/generate_flashcards", "Flashcards"),
        ("/generate_mcqs", "MCQs"),
        ("/generate_fillups", "Fill-in-the-Blanks"),
        ("/generate_mindmap", "Mindmap"),
        ("/generate_schedule", "Study Schedule"),
        ("/generate_summary", "AI Summary")
    ]
    
    print("\n🔧 Testing Feature Generation:")
    print("-" * 30)
    
    for endpoint, feature_name in endpoints:
        try:
            response = requests.post(
                base_url + endpoint,
                json={"text": test_text},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    print(f"⚠️  {feature_name}: {result['error']}")
                else:
                    print(f"✅ {feature_name}: Generated successfully")
            else:
                print(f"❌ {feature_name}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {feature_name}: Error - {str(e)}")
    
    # Test 3: Test chatbot
    print("\n🤖 Testing Chatbot:")
    print("-" * 20)
    
    try:
        response = requests.post(
            base_url + "/chatbot",
            json={
                "question": "What is machine learning?",
                "context": test_text
            },
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"⚠️  Chatbot: {result['error']}")
            else:
                print(f"✅ Chatbot: Response generated successfully")
        else:
            print(f"❌ Chatbot: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Chatbot: Error - {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\nTo use the application:")
    print("1. Open your browser")
    print("2. Go to http://localhost:5000")
    print("3. Upload a document and start learning!")

if __name__ == "__main__":
    test_app() 
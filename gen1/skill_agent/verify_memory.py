import requests
import time

BASE_URL = "http://localhost:8000"

def test_memory():
    print("--- Testing Chat Memory ---")
    
    # 1. Set Context
    payload1 = {
        "task_description": "Hello, my name is Pratik. Remember this.",
        "extra_inputs": {}
    }
    print(f"\nUser: {payload1['task_description']}")
    response1 = requests.post(f"{BASE_URL}/api/v1/run", json=payload1).json()
    
    if not response1.get("success"):
        print(f"Error Turn 1: {response1.get('message')}")
        return
        
    thread_id = response1["thread_id"]
    print(f"Agent: {response1['result'][:100]}...")
    print(f"Thread ID: {thread_id}")
    
    # 2. Verify Context
    payload2 = {
        "task_description": "What is my name? And who am I talking to?",
        "thread_id": thread_id,
        "extra_inputs": {}
    }
    print(f"\nUser: {payload2['task_description']}")
    response2 = requests.post(f"{BASE_URL}/api/v1/run", json=payload2).json()
    
    if not response2.get("success"):
        print(f"Error Turn 2: {response2.get('message')}")
        return
        
    print(f"Agent: {response2['result']}")
    
    if "Pratik" in response2["result"]:
        print("\n✅ Memory Test Passed: Agent remembered the name.")
    else:
        print("\n❌ Memory Test Failed: Agent forgot the name.")

if __name__ == "__main__":
    try:
        test_memory()
    except Exception as e:
        print(f"Connection failed: {e}")

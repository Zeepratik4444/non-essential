import requests
import json
import time

BASE_URL = "http://localhost:8000"

def run_task(description: str, extra_inputs: dict = None):
    """Send a task request to the Skill Agent API."""
    url = f"{BASE_URL}/api/v1/run"
    payload = {
        "task_description": description,
        "extra_inputs": extra_inputs or {}
    }
    
    print(f"\n🚀 [EXECUTION] Task: {description[:100]}...")
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=300)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                print(f"✅ Executed in {duration:.2f}s")
                return data["result"]
            else:
                print(f"❌ API Error: {data['message']}")
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    return None

def assess_result(task_description: str, final_result: str):
    """Ask the agent to assess its own previous output based on quality standards."""
    assessment_prompt = (
        f"ASSESSMENT TASK: Evaluate the following result against the standards for its domain. "
        f"Does it follow the protocol? Is it accurate? Is the format correct? "
        f"Return a score (1-10) and brief justification.\n\n"
        f"ORIGINAL TASK: {task_description}\n\n"
        f"RESULT TO ASSESS:\n{final_result}"
    )
    
    print(f"🔍 [ASSESSMENT] Analyzing performance...")
    assessment = run_task(assessment_prompt)
    if assessment:
        print("\n📊 ASSESSMENT REPORT:")
        print(assessment)
    return assessment

def test_domain(name: str, task: str):
    print(f"\n" + "="*80)
    print(f" TESTING DOMAIN: {name.upper()}")
    print("="*80)
    
    result = run_task(task)
    if result:
        # Show first 500 chars of result
        preview = result[:500] + ("..." if len(result) > 500 else "")
        print(f"\nRESULT PREVIEW:\n{preview}")
        
        # Assess it
        assess_result(task, result)
    else:
        print(f"🛑 Failed to get result for {name}")

def main():
    domains = [
        {
            "name": "Financial Analysis",
            "task": "Analyze the profitability of a SaaS company with $10M ARR, $2M COGS, and $5M OpEx. Calculate Gross Margin and EBITDA Margin."
        },
        {
            "name": "Legal Review",
            "task": "Review a standard NDAs 'Confidential Information' clause. Identify if it's too broad and suggest a standard carve-out for publicly known information."
        },
        {
            "name": "HR Recruitment",
            "task": "Draft a job description for a Senior DevOps Engineer. Include key responsibilities, required technical stack (AWS, K8s, Terraform), and success metrics."
        },
        {
            "name": "Customer Support",
            "task": "Draft a response to a customer who is angry about a 24-hour service outage. Be empathetic, explain we are working on it, and offer a 10% credit."
        },
        {
            "name": "Code Review",
            "task": "Review this Python snippet for security risks: `cursor.execute('SELECT * FROM users WHERE id = ' + user_id)`. Explain the risk and provide the fix."
        }
    ]

    for domain in domains:
        test_domain(domain["name"], domain["task"])
        print("\n" + "Waiting for next test..." + "\n")
        time.sleep(2)

if __name__ == "__main__":
    print("=== SKILL AGENT - MULTI-DOMAIN AUTOMATED TEST & ASSESSMENT ===")
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5).json()
        print(f"System Status: ONLINE (v{health['version']})")
        main()
    except Exception as e:
        print(f"❌ Server unreachable: {e}. Ensure 'python main.py' is running.")

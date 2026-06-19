import json
import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

# Sample ticket data (Chaotic input)
messy_email = """
Hello, I am extremely frustrated!!! I ordered a premium stainless steel tumbler 
(Order #98765) last week for my wife's birthday party which is tomorrow. The tracking page 
says it hasn't even left your warehouse yet! This is completely unacceptable customer service. 
If it doesn't arrive by tomorrow morning, I want a full refund immediately and I will cancel 
my subscription. Also, your checkout page charged me twice for shipping, please fix that too. 
Not happy at all.
- Marcus Jenkins
"""

def analyze_customer_email(email_text):
    """[Phase 1] Sends raw text to Ollama and enforces strict JSON output."""
    print("🤖 Processing raw email text through local intelligence engine...")
    
    system_instruction = """
    You are an automated corporate customer support intelligence data node. 
    Analyze the incoming customer email and extract core tracking metrics.
    
    You MUST return a valid JSON object matching this exact schema layout:
    {
        "customer_name": "String representing customer name",
        "order_id": "String representing order number or null if missing",
        "sentiment": "Must be either 'Positive', 'Neutral', or 'Negative'",
        "primary_category": "Must be either 'Billing', 'Delivery Delay', 'Product Defect', or 'General Inquiry'",
        "urgency_score": An integer scale from 1 (very low priority) to 5 (critical fire emergency),
        "one_sentence_summary": "A brief, professional summary distilling the core problem."
    }
    Return raw JSON only. Do not include markdown code block formats or backticks.
    """
    
    full_prompt = f"{system_instruction}\n\nCustomer Email Content:\n{email_text}"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "format": "json"
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code == 200:
            return json.loads(response.json()['response'])
        return None
    except Exception as e:
        print(f"❌ Pipeline Ingestion Failed: {e}")
        return None

# ==========================================================
# PHASE 2: THE AUTOMATED ROUTING ENGINE
# ==========================================================
def route_customer_ticket(ticket_metadata):
    """
    Applies standard enterprise conditional logic to dispatch 
    the data payload to the target operational department queue.
    """
    print("🔀 Evaluating business logic routing matrices...")
    
    # 1. Read the parameters extracted by our AI phase
    category = ticket_metadata.get("primary_category")
    urgency = ticket_metadata.get("urgency_score", 1)
    sentiment = ticket_metadata.get("sentiment")
    
    # 2. Establish the target destination file name based on logic gates
    if urgency == 5 or category == "Billing":
        queue_destination = "queue_CRITICAL_ESC.json"
        routing_reason = "🚨 Escalated due to Critical Urgency (Score 5) or Billing Dispute."
        
    elif category == "Delivery Delay":
        queue_destination = "queue_LOGISTICS.json"
        routing_reason = "📦 Routed to Operations & Logistics for fulfillment check."
        
    elif category == "Product Defect":
        queue_destination = "queue_QA_ENGINEERING.json"
        routing_reason = "🛠️ Routed to Quality Assurance & Product Engineering."
        
    elif sentiment == "Positive":
        queue_destination = "queue_MARKETING.json"
        routing_reason = "✨ Routed to Marketing & Growth for testimonial acquisition."
        
    else:
        queue_destination = "queue_GENERAL_SUPPORT.json"
        routing_reason = "📥 Routed to Standard Support Tier Customer Queue."

    print(f"-> Decision: {routing_reason}")
    print(f"-> Dispatching to destination folder payload: '{queue_destination}'")
    
    # 3. Persistence: Write the data asset to its designated file path
    # If the file already exists, we load it, append the new ticket, and resave it
    existing_queue = []
    if os.path.exists(queue_destination):
        try:
            with open(queue_destination, "r") as f:
                existing_queue = json.load(f)
        except Exception:
            existing_queue = []
            
    existing_queue.append(ticket_metadata)
    
    with open(queue_destination, "w") as f:
        json.dump(existing_queue, f, indent=4)
        
    print(f"✅ Securely written to {queue_destination} successfully.")


# ==========================================================
# EXECUTION LAYER
# ==========================================================
if __name__ == "__main__":
    # Execute Phase 1: Ingestion and AI Classification
    insights = analyze_customer_email(messy_email)
    
    # Execute Phase 2: System Routing Real-Time Dispatch
    if insights:
        print("\n--- Starting Phase 2 Data Dispatch ---")
        route_customer_ticket(insights)
    else:
        print("❌ Pipeline execution aborted due to upstream metadata absence.")
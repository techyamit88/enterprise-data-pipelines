import time
from triage_pipe import analyze_customer_email, route_customer_ticket

# A realistic pool of incoming enterprise customer complaints
simulated_inbox = [
    "Hey! My package was supposed to arrive today but the tracker says it's stuck in Chicago. Please help, it's a gift! - Sarah T.",
    "I was looking at your catalog and I just wanted to say your new premium tumblers look amazing! Great design guys. - David K.",
    "URGENT: Your system charged my credit card three times for order #11223! I need an immediate reversal or I will call my bank. - Elena R.",
    "The handle on the flask I bought yesterday completely snapped off on my first run. The build quality feels very cheap. - John D.",
    "Can you tell me if your drinkware products are completely dishwasher safe? I couldn't find it on the FAQ page. - Linda M.",
    "My order #55443 is missing the extra custom lids I paid for. The box only had the base tumbler. Please send them. - Robert H."
]

print("🚀 Initializing Bulk Customer Feed Simulation Stream...")
print(f"📦 Total incoming queue load: {len(simulated_inbox)} text documents.")
print("--------------------------------------------------")

for index, email in enumerate(simulated_inbox):
    print(f"\n[Incoming Packet {index + 1}/{len(simulated_inbox)}]")
    
    # 1. Run through your Phase 1 AI processing node
    extracted_insights = analyze_customer_email(email)
    
    # 2. Run through your Phase 2 routing dispatcher node
    if extracted_insights:
        route_customer_ticket(extracted_insights)
        
    # Introduce a slight delay to respect your local machine's computing processing cycles
    time.sleep(1)

print("\n✨ Simulation complete! Refresh your Streamlit browser window now!")
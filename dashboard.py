import streamlit as st
import pandas as pd
import json
import os
import glob

# Set page configurations
st.set_page_config(page_title="SmartQueue Analytics", layout="wide", page_icon="📊")

st.title("📊 SmartQueue: Enterprise Triage & Insights Dashboard")
st.markdown("Real-time operational visibility into automated AI customer support routing channels.")
st.markdown("---")

def load_all_queue_data():
    """Scans the directory for department queue files and merges the records."""
    all_tickets = []
    
    # Locate any file matching the pattern 'queue_*.json'
    queue_files = glob.glob("queue_*.json")
    
    for file_path in queue_files:
        # Extract the department name from the filename (e.g., queue_LOGISTICS.json -> LOGISTICS)
        dept_name = file_path.replace("queue_", "").replace(".json", "")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    # Add department metadata tag to each ticket item
                    for ticket in file_data:
                        ticket["assigned_department"] = dept_name
                        all_tickets.append(ticket)
            except Exception:
                pass
                
    return all_tickets

# 1. Fetch data payload from local system files
raw_tickets = load_all_queue_data()

if not raw_tickets:
    st.warning("📥 No active ticket files found in the directory. Run 'triage_pipe.py' to generate data records!")
else:
    # Convert our list of JSON dicts into a clean Pandas DataFrame for analytical processing
    df = pd.DataFrame(raw_tickets)

    # ==========================================================
    # KIP METRICS ROW
    # ==========================================================
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Ingested Tickets", value=len(df))
        
    with col2:
        # Calculate critical high-priority counts safely
        critical_count = len(df[df['urgency_score'] >= 4]) if 'urgency_score' in df.columns else 0
        st.metric(label="🚨 High Urgency (Score 4-5)", value=critical_count)
        
    with col3:
        # Isolate negative sentiments that require high-touch communication
        neg_count = len(df[df['sentiment'] == 'Negative']) if 'sentiment' in df.columns else 0
        st.metric(label="🛑 Negative Sentiment Inbound", value=neg_count)
        
    with col4:
        # Count target departments active
        dept_count = df['assigned_department'].nunique() if 'assigned_department' in df.columns else 0
        st.metric(label="🏢 Active Operating Queues", value=dept_count)

    st.markdown("---")

    # ==========================================================
    # DATA GRID & INSPECTION TIERS
    # ==========================================================
    st.subheader("📋 Active Customer Priority Matrix")
    st.markdown("Select, sort, or filter through live records parsed by the local AI engine.")
    
    # Re-organize layout columns for professional scannability
    desired_columns = ["customer_name", "order_id", "primary_category", "urgency_score", "sentiment", "assigned_department", "one_sentence_summary"]
    available_columns = [col for col in desired_columns if col in df.columns]
    
    # Display the reactive data grid
    st.dataframe(df[available_columns], use_container_width=True, hide_index=True)

    st.markdown("---")

    # ==========================================================
    # GRAPHICAL METRIC DISTRIBUTION
    # ==========================================================
    st.subheader("📈 Queue Volumetric Distributions")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("**Tickets Volume by Target Department**")
        if 'assigned_department' in df.columns:
            dept_counts = df['assigned_department'].value_counts()
            st.bar_chart(dept_counts)
            
    with chart_col2:
        st.markdown("**Urgency Distribution Metrics**")
        if 'urgency_score' in df.columns:
            urgency_counts = df['urgency_score'].value_counts().sort_index()
            st.bar_chart(urgency_counts)
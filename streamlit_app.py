import streamlit as st
import requests
import os
import plotly.io as pio
import plotly.graph_objects as go

# Set up the Streamlit app
st.title("Data Analysis with GPT-4")

# Input for the question
question = st.text_input("Enter your question:")

# Button to send the request
if st.button("Analyze"):
    if question:
        # Send the request to the Flask backend
        response = requests.post("http://127.0.0.1:5000/analyze", json={"question": question})
        
        if response.status_code == 200:
            data = response.json().get("data")
            analysis = response.json().get("analysis")

            # Display the data
            st.subheader("Data")
            st.text_area("Data", data, height=200)
            st.subheader("Analysis")
            st.text_area("Analysis", analysis, height=200)
            st.subheader("Figure")
            st.image("figure.png", caption="Generated Figure", use_column_width=True)
            
            # Notification input section
            st.subheader("Notify me when")
            notification_message = st.text_input("Enter your notification message:", key="notification_input")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Email Notification"):
                    st.text("Email notification set!")
            
            with col2:
                if st.button("Phone Notification"):
                    st.text("Phone notification set!")
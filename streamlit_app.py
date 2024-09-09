import streamlit as st
import requests
import json
from PIL import Image
import io

# Set up the Streamlit app
st.title("Data Analysis with GPT-4")

# Define the endpoint
BACKEND_ENDPOINT = "http://172.17.0.4:8080"

# Input for the question
question = st.text_input("Enter your question:")

# Button to send the request
if st.button("Analyze"):
    if question:
        # Make a POST request to your Flask backend
        response = requests.post(f"{BACKEND_ENDPOINT}/analyze", json={"question": question})
        
        if response.status_code == 200:
            result = response.json()
            
            # Display analysis
            st.subheader("Analysis")
            st.write(result['analysis'])
            
            # Display generated code
            st.subheader("Generated Code")
            st.code(result['generated_code'], language='python')
            
            # Display execution times
            st.subheader("Execution Times")
            st.write(f"Code Generation Time: {result['code_generation_time']:.2f} seconds")
            st.write(f"Code Execution Time: {result['code_execution_time']:.2f} seconds")
            
            # Get and display the image
            image_url = f"{BACKEND_ENDPOINT}{result['image_url']}"
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image = Image.open(io.BytesIO(image_response.content))
                st.image(image, caption="Generated Chart", use_column_width=True)
            else:
                st.error("Failed to retrieve the image.")
            
            # Display data (optional, as it's already visualized in the chart)
            # st.subheader("Data")
            # st.write(result['data'])
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    else:
        st.warning("Please enter a question.")

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
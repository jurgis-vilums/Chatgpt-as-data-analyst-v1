
import subprocess

# Start main.py
subprocess.Popen(['python', 'main.py'])

# Start Streamlit app
subprocess.Popen(['streamlit', 'run', 'streamlit_app.py'])

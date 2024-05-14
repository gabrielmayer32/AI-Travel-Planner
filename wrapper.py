# wrapper.py
import os
import sys
from streamlit.web import cli as stcli

# wrapper.py
import subprocess

def app():
    cmd = ["streamlit", "run", "app.py"]
    process = subprocess.Popen(cmd)
    process.communicate()

if __name__ == "__main__":
    app()

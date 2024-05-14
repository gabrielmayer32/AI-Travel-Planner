# wrapper.py
import os
import sys
from streamlit.web import cli as stcli

def app():
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    app()

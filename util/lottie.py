""" 
This module manages lottie animations in the app.

Reference: 
1) GitHub: https://github.com/andfanilo/streamlit-lottie
2) Lottie Files: https://lottiefiles.com/

"""

import json
import requests  # pip install requests


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

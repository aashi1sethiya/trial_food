
# Interactive Food Carbon and Nutrition Dashboard with Python – Streamlit

Food carbon and nutrition label Dashboard built in Python and the Streamlit library to visualize and track carbon footprint and macronutrients of your meals.

## Author
- Matthew Cheng 


## Setup 
To launch:
* `cd` to directory of this `README.md`
* Run `pip install -r requirements.txt`
* Run `streamlit run app.py`
* Browser will open with the webapp.

To expose local port to public url (ngrok):
* `pip install pyngrok`
* Open a terminal to start ngrok tunnel to listen in on a local port (see `ngrok.sh`): `ngrok http 8501`
* Run the web app on the same port number (see `streamlit.sh`): `streamlit run --server.port 8501 app.py >/dev/null`
* Now navigate to [ngrok](https://dashboard.ngrok.com/cloud-edge/status) and open one of the urls to see your web app.
* To kill the session, press `Ctrl + C` in the terminal running ngrok and the tunnel session will be killed. 

## Todo
- Hosting: Similar to sjcam local http server

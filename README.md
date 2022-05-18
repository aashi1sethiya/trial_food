
# Interactive Food Carbon and Nutrition Dashboard with Python – Streamlit

Food carbon and nutrition label Dashboard built in Python and the Streamlit library to visualize and track carbon footprint and macronutrients of your meals.

## Author
- Matthew Cheng 

## Introduction
Did you know that our eating habits have a direct impact on the planet? About 26% of global greenhouse gas emissions are fuelled by food production [1], contributing significantly to climate change. 

The good news? Simple changes to our daily lives can have huge impact – like eating a more nutrient- dense plant-based diet, using less single-use plastic and reducing edible food waste, we can cut our collective greenhouse gas emissions significantly. 

“The Climate Diet” app helps you plan your meal at Team Dining to create delicious, nutritious and low-carbon meals, giving you the power to manage your health and protect the environment! 


[1] Poore, J., & Nemecek, T. (2018). Reducing food’s environmental impacts through producers and consumers. Science, 360(6392), 987-992.

## Setup 
To launch:
* `cd` to directory of this `README.md`
* Run `pip install -r requirements.txt`
* Run `streamlit run app.py`
* Browser will open with the webapp.

To expose local port to public url (ngrok):
* `pip install pyngrok`
* `pip install cachetools`
* Open a terminal to start ngrok tunnel to listen in on a local port (see `ngrok.sh`): `ngrok http 8501`
* Run the web app on the same port number (see `streamlit.sh`): `streamlit run --server.port 8501 app.py >/dev/null`
* Now navigate to [ngrok](https://dashboard.ngrok.com/cloud-edge/status) and open one of the urls to see your web app.
* To kill the session, press `Ctrl + C` in the terminal running ngrok and the tunnel session will be killed. 

To deploy on Google Cloud Run:
* Build the app: `gcloud builds submit --tag gcr.io/ProjectID/AppName --project=ProjectID --timeout=3600s` (N.B. the 1 hour timeout parameter, so the build doesn't prematurely timeout)
* Deploy the app: `gcloud run deploy --image gcr.io/ProjectID/AppName --project=ProjectID --platform managed --allow-unauthenticated`


## Todo

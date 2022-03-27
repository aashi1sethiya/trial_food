# Use the official lightweight python image.
FROM python:3

# Allow statements and log messages to immediately appear in the native logs
ENV PYTHONUNBUFFERED 1

# Expose port 8080 to serve the app
EXPOSE 8080

# Copy local code to the container image
WORKDIR /usr/src/app
COPY . .

# install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Run `streamlit run` command on container startup. Here we use the gunicorn 
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to ve equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run
# to handle instance scaling.
CMD streamlit run --server.port 8080 --server.enableCORS false app.py
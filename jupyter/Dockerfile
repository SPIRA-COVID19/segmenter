# Use an official Python runtime as a parent image
FROM python:3.9
# Set the working directory to /jupyter
WORKDIR /jupyter
# install necessary build packages
RUN  apt-get update && apt-get install -y gcc libsndfile1-dev
# Copy the current directory contents into the container at /jupyter
COPY requirements.txt /jupyter
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org --no-cache -r requirements.txt && jupyter-nbextension enable rise --py
# Make port 8888 available to the world outside this container
EXPOSE 8888

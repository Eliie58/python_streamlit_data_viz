# Barcelona through Data

## Introduction
In this repositiry, you will find the code to run a streamlit web application, that uses publicly available data, related to Barcelona, to try and help the people moving to Barcelona, to find the best suiting District for them.
This is a data visualization project prepared by students @ EPITA for the class of "Data Reporting and Visualization" during June 2022.

## Data
The data used is from https://www.kaggle.com/datasets/xvivancos/barcelona-data-sets

## Requirements
This streamlit web app runs on Python 3.6
Requirements are:

* streamlit 
* pandas 
* numpy
* plotly

## Running streamlit

To run this streamlit web application, from the root of the project run:
```
streamlit run Introduction.oy
```

## Docker

This application can also be deployed using Docker, using the available Dockerfile.
To build and run the docker image:
```
docker build --pull --rm -f "Dockerfile" -t barcelona:latest "."
docker run -p 8501:8501 barcelona:latest
```

## Demo

To view a demo of this project, you can go [here](https://python-streaml-prod-streamlit-barcelona-jel6zd.mo2.mogenius.io/)<br>
Hosted with [Mogenius](https://mogenius.com/home)
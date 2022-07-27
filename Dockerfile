FROM python:3.6
WORKDIR /app

RUN pip install streamlit pandas plotly
EXPOSE 8501
COPY Introduction.py .
COPY pages/ ./pages

COPY archive/ ./archive

ENTRYPOINT ["streamlit", "run"]

CMD ["Introduction.py"]
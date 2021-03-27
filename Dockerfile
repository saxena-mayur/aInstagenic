FROM python:3.7.2-slim

EXPOSE 8501

WORKDIR .
COPY requirements.txt .
COPY app.py .
COPY config.json ./

RUN apt-get -y update && apt-get install -y libzbar-dev

RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

ENTRYPOINT [ "streamlit", "run"]
CMD ["app.py"]
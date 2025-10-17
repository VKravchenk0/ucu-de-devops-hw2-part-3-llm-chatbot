FROM python:3.13-slim

# todo remove
RUN apt-get -y update; apt-get -y install curl

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .

EXPOSE 8050

CMD ["streamlit", "run", "app.py", "--server.port=8050", "--server.address=0.0.0.0"]
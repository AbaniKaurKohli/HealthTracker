FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl

COPY . /app/

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_frontend.py"]

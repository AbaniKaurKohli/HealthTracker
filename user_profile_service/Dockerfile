FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "user_service:app"]


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests

COPY . /app/

EXPOSE 5001

CMD ["python", "user_service.py"]

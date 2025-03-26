FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
# Entry point script to run migrations before starting the app
CMD ["sh", "-c", "flask db upgrade && python app.py"]
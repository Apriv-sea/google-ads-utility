FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY .streamlit/ .streamlit/

EXPOSE 8080
CMD streamlit run --server.port=8080 --browser.serverAddress=0.0.0.0 src/main.py

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY streamlit_app.py /app/
COPY artifacts/data_preprocessing/. /app/artifacts/data_preprocessing/
COPY artifacts/train_model/. /app/artifacts/train_model/
COPY params/. /app/params/
COPY test.py /app/

EXPOSE 8501

CMD ["streamlit", "run", "--server.port", "8501", "streamlit_app.py"]
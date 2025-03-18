FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install elasticsearch
RUN pip install dotenv
EXPOSE 5000
CMD ["python3", "app.py"]

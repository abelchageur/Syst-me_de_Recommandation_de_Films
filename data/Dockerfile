FROM bitnami/spark:latest

# Install Jupyter and dependencies

RUN pip install jupyter
RUN pip install pandas
RUN pip install py4j
RUN pip install Elasticsearch
RUN pip install dotenv
WORKDIR /opt/spark-data

# Expose Jupyter port
EXPOSE 8888


# Start Jupyter Notebook
CMD ["python", "-m", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]
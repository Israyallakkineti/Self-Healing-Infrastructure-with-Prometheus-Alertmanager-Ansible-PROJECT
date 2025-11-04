FROM python:3.11-slim
WORKDIR /webhook
COPY app.py /webhook/
RUN pip install flask
RUN apt-get update && apt-get install -y \
    sshpass ansible \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/bin:${PATH}"
CMD ["python", "/webhook/app.py"]


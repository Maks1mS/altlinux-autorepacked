FROM registry.altlinux.org/alt/python:p10

RUN apt-get update && apt-get install -y \
    eepm \
    wget
#    && rm -rf /var/lib/apt/lists/*

COPY ./autorepacked ./autorepacked

ENV PYTHONPATH "${PYTHONPATH}:."

CMD ["python3", "-u", "./autorepacked/main.py"]
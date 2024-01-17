FROM registry.altlinux.org/alt/python:p10

RUN apt-get update && apt-get install -y \
    wget \
    apt-repo-tools \
    alien \
    pip && \
    wget -O- https://eepm.ru/epm.sh | bash /dev/stdin ei
#    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip --no-cache-dir install -r requirements.txt

COPY ./autorepacked ./autorepacked

ENV PYTHONPATH "${PYTHONPATH}:."

CMD ["python3", "-u", "./autorepacked/main.py"]
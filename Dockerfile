FROM python:3.11-slim

# Install nsjail dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3-pip \
    libcap-dev \
    libprotobuf-dev \
    protobuf-compiler \
    pkg-config \
    zlib1g-dev \
    libnl-route-3-dev \
    curl \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Install nsjail
RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && \
    make && \
    cp nsjail /usr/local/bin/ && \
    cd .. && rm -rf nsjail

WORKDIR /app

COPY app/ /app/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python3", "main.py"]

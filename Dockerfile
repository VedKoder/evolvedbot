FROM nikolaik/python-nodejs:python3.10-nodejs19

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -U pip setuptools wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Default command (works for Railway, Koyeb, and Heroku)
CMD ["python3", "-m", "SHUKLAMUSIC"]

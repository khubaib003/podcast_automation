# FROM python:3.10

# WORKDIR /files

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["python", "flask_generating_video.py"]















FROM python:3.10-slim

# Install system dependencies
RUN apt update && apt install -y ffmpeg

# Install Playwright Browsers
RUN pip install playwright && playwright install --with-deps

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set working dir
WORKDIR /files



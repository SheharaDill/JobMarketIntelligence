# --------------------------------------------------
# Base Image
# --------------------------------------------------
# Uses official Python image.
#
# Python 3.12 is stable and modern.
# --------------------------------------------------

FROM python:3.12-slim


# --------------------------------------------------
# Working Directory
# --------------------------------------------------
# Everything inside container
# will live here.
# --------------------------------------------------

WORKDIR /app


# --------------------------------------------------
# Copy Requirements
# --------------------------------------------------
# Copy requirements first so
# Docker can cache dependencies.
# --------------------------------------------------

COPY requirements.txt .

# --------------------------------------------------
# Install Google Chrome + Dependencies
# --------------------------------------------------

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libgcc-s1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
    | gpg --dearmor -o /usr/share/keyrings/google.gpg

RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google.list

RUN apt-get update && apt-get install -y \
    google-chrome-stable
RUN which google-chrome

RUN google-chrome --version    

# --------------------------------------------------
# Install Dependencies
# --------------------------------------------------


RUN pip install --no-cache-dir -r requirements.txt


# --------------------------------------------------
# Copy Project Files
# --------------------------------------------------

COPY . .


# --------------------------------------------------
# Start Platform
# --------------------------------------------------
# Runs your launcher:
#
# Initial Scrape
# Scheduler
# Flask API
# --------------------------------------------------

CMD ["python", "main.py"]
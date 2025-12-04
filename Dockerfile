FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git gcc g++ make python3-dev python3-pip \
    libxml2-dev libxslt1-dev zlib1g-dev \
    gettext curl redis-server \
    default-libmysqlclient-dev pkg-config \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

# Install Node.js build tools
RUN npm install -g sass postcss-cli postcss autoprefixer

WORKDIR /site

# Clone DMOJ repository
RUN git clone --recursive https://github.com/DMOJ/online-judge.git . && \
    git submodule update --init --recursive

# Install Python dependencies
# FIXED: Added django-redis
RUN pip3 install --no-cache-dir "setuptools<70.0.0" && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip3 uninstall -y websocket || true && \
    pip3 install --no-cache-dir mysqlclient gunicorn gevent websocket-client django-redis

# Create directories
RUN mkdir -p /site/resources /site/media /site/pdfcache /site/datacache /problems

# Copy configuration
COPY local_settings.py /site/dmoj/local_settings.py

EXPOSE 8000

CMD ["gunicorn", "dmoj.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "gevent", \
     "--worker-connections", "1000", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]

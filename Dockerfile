FROM ubuntu:22.04

RUN apt update -y && apt install -y \
    git build-essential gcc g++ make python3 python3-dev python3-pip python3-venv python3-wheel \
    default-libmysqlclient-dev pkg-config libxml2-dev libxslt1-dev zlib1g-dev gettext curl redis-server \
    mariadb-server nodejs npm supervisor nginx \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN npm install -g sass postcss-cli postcss autoprefixer

WORKDIR /usr/local/app

RUN git clone https://github.com/DMOJ/site.git

WORKDIR /usr/local/app/site

RUN git submodule init && git submodule update

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt mysqlclient uwsgi websocket-client mysql-connector-python

ENV PATH="/usr/local/app/site/venv/bin:$PATH"

COPY entrypoint.sh /usr/local/app/entrypoint.sh
RUN chmod +x /usr/local/app/entrypoint.sh

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80 443

ENTRYPOINT ["/usr/local/app/entrypoint.sh"]

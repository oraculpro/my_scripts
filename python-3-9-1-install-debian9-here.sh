#!/bin/bash

sudo apt-get update; \
sudo apt-get install build-essential checkinstall; \
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev \
libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev; \
wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz; \
tar xzf Python-3.9.1.tgz; \
cd Python-3.9.1; \
sudo ./configure --enable-optimizations; \
sudo make altinstall; \
Python3.9 -V;
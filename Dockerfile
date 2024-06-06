FROM python:2.7
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    python-pip libsuitesparse-dev gfortran
RUN pip install -U "scipy==1.2"
RUN pip install -U "numpy"
RUN pip install -U "networkx"
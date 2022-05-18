# FROM python:3
FROM odoo:15

WORKDIR /usr/bin/python

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r -U requirements.txt

#COPY . . 

# CMD ["python"]
FROM python:latest

COPY py_requirements.txt /

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r py_requirements.txt

COPY . .
# COPY src/*.py /

CMD ["python","./src/main.py"]

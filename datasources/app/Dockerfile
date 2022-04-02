FROM python:3.10.4
WORKDIR /code
COPY dbExp.py ./
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN echo "done installing dependencies"
CMD ["python", "-u", "dbExp.py"]
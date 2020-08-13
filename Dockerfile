FROM python:3.7
COPY . /pharma_api
WORKDIR /pharma_api
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
FROM python:3.7

RUN echo testestestest
COPY . /app
WORKDIR /app
RUN echo testestestest
RUN pip install -r requirements.txt
EXPOSE 5000

RUN echo testestestest2
CMD ["python3", "flask_page.py"]
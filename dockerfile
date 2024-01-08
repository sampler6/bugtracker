FROM python:3.11.4

RUN mkdir /bug_tracker

WORKDIR /bug_tracker

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY . .
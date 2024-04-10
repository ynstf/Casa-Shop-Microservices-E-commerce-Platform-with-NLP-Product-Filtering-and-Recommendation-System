FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN python3 -m venv /opt/venv
COPY requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt
COPY . .

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

EXPOSE 5550

CMD ["/app/entrypoint.sh"]
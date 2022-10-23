# Dockerfile

FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install nginx
RUN apt-get update && apt-get install nginx -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default

# copy source and install dependencies
COPY . /anorum/
WORKDIR /anorum
RUN pip install -r requirements.txt

# start server
EXPOSE 80
EXPOSE 443
CMD ["/anorum/start_server.sh"]

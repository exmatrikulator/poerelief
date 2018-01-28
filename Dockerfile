FROM alpine

# expose web server port
# only http, for ssl use reverse proxy
EXPOSE 80

#build tools for Flask-SQLAlchemy-->cffi
RUN apk add --no-cache bash git nginx uwsgi uwsgi-python py2-pip python2-dev libffi-dev alpine-sdk \
	&& pip install --upgrade pip


# application folder
ENV APP_DIR /app

# app dir
COPY . ${APP_DIR}
COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod 777 -R /run/
WORKDIR ${APP_DIR}

RUN pip install -r ${APP_DIR}/requirements-py2.txt

# exectute start up script
ENTRYPOINT ["/app/entrypoint.sh"]

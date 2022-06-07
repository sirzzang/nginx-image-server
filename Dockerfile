FROM python:3.9-slim-bullseye

# build args
ARG NGINX_VERSION
ARG UPLOAD_MODULE_VERSION

# install dependencies
RUN apt-get update \
    && apt-get install -y wget gcc g++ make \
    && apt-get install -y fcgiwrap zlib1g zlib1g-dev openssl libssl-dev libpcre3 libpcre3-dev

# create nginx user/group and add nginx user to nginx group
RUN addgroup --system --gid 102 nginx \
    && adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 102 nginx

# compile and build nginx with nginx upload module
RUN set -x \
    && wget -P /usr/src "https://github.com/vkholodkov/nginx-upload-module/archive/${UPLOAD_MODULE_VERSION}.tar.gz" \
    && tar -xzvf /usr/src/$UPLOAD_MODULE_VERSION.tar.gz -C /usr/src \
    && wget -P /usr/src "https://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" \
    && tar -xzvf /usr/src/nginx-$NGINX_VERSION.tar.gz -C /usr/src \
    && cd /usr/src/nginx-$NGINX_VERSION \
    && CONFIG="\
    --user=nginx \
    --group=nginx \
    --sbin-path=/usr/local/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/var/run/nginx/nginx.pid \
    --lock-path=/var/lock/nginx/nginx.lock \
    --http-log-path=/var/log/nginx/access.log \
    --error-log-path=/var/log/nginx/error.log \
    --with-debug \
    --with-compat \
    --add-module=/usr/src/nginx-upload-module-${UPLOAD_MODULE_VERSION} \
    " \
    && ./configure $CONFIG \
    && make -j $(getconf _NPROCESSORS_ONLN) \
    && make install \
    && mkdir /var/lock/nginx \
    && mkdir /etc/nginx/conf.d/ \
    && mkdir /usr/local/nginx/scripts/

# change owners
RUN chown nginx:nginx -R /etc/nginx/conf.d \
    && chown nginx:nginx -R /usr/local/nginx/scripts

# make file directories
RUN mkdir /images \
    && mkdir /documents \
    && chown nginx:nginx -R /images \
    && chown nginx:nginx -R /documents \
    && chmod 766 -R /images \
    && chmod 766 -R /documents

# forward request, error logs to nginx-image-server Docker
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stdout /var/log/nginx/error.log \
    && mkdir /docker-entrypoint.d

# docker entrypoint
COPY docker-entrypoint.sh /
COPY fcgiwrap.sh /docker-entrypoint.d
RUN chmod +x docker-entrypoint.sh \
    && chmod +x -R /docker-entrypoint.d
ENTRYPOINT ["/docker-entrypoint.sh"]

# nginx server listening port
EXPOSE ${MEDIA_PORT}

# stopsignal
STOPSIGNAL SIGQUIT

# disable nginx daemon mode
CMD ["nginx", "-g", "daemon off;"]

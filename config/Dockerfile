FROM prestashop/prestashop:1.7.8

RUN a2enmod ssl
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

RUN rm -rf /var/www/html/*
COPY --chmod=777 ./prestashop-source/ /var/www/html/
COPY ./config/ssl /etc/apache2/ssl
COPY ./config/ssl/000-default.conf /etc/apache2/sites-available/000-default.conf

COPY ./config/mariadb/BE_196638.sql /tmp/BE_196638.sql
COPY ./config/init_db.sh /tmp/init_db.sh

RUN mkdir -p /var/www/html/var/logs
RUN chmod -R 777 /var/www/html/var
RUN chmod +x /tmp/init_db.sh

EXPOSE 443

ENTRYPOINT ["/tmp/init_db.sh"]
FROM prestashop/prestashop:1.7.8

RUN a2enmod ssl

RUN rm -rf /var/www/html/*
COPY --chmod=777 ./prestashop-source/ /var/www/html/

COPY ./config/ssl /etc/apache2/ssl
COPY ./config/ssl/000-default.conf /etc/apache2/sites-available/000-default.conf

RUN mkdir -p /var/www/html/var/logs
RUN chmod -R 777 /var/www/html/var

EXPOSE 443
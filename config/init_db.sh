#!/bin/sh
set -e

DB_HOST="admin-mysql_db"
DB_USER="root"
DB_PASS="student"
DB_NAME="BE_196638"

echo "Waiting for database connection on $DB_HOST..."

until mysqladmin ping -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" --silent; do
    echo "Database is not reachable yet. Sleeping 5s..."
    sleep 5
done

echo "Database is UP! Checking for tables in $DB_NAME..."

TABLE_COUNT=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "SHOW TABLES;" | wc -l)

if [ "$TABLE_COUNT" -le 1 ]; then
    echo "Database is empty. Starting import from /tmp/BE_196638.sql..."
    mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" < /tmp/BE_196638.sql
    echo "Success: Initialization complete."
else
    echo "Database already has $TABLE_COUNT tables. Skipping initialization."
fi

echo "Forcing performance settings (Cache ON)..."
mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" -e "
  UPDATE ps_configuration SET value='1' WHERE name='PS_SMARTY_CACHE';
  UPDATE ps_configuration SET value='1' WHERE name='PS_CSS_THEME_CACHE';
  UPDATE ps_configuration SET value='1' WHERE name='PS_JS_THEME_CACHE';
  UPDATE ps_configuration SET value='0' WHERE name='PS_SMARTY_FORCE_COMPILE';
"
echo "Performance settings updated."

echo "Launching PrestaShop..."
exec /tmp/docker_run.sh
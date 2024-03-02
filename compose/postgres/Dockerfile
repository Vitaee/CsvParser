FROM postgis/postgis:14-3.4


RUN echo "CREATE EXTENSION IF NOT EXISTS pg_trgm;" >> /docker-entrypoint-initdb.d/init.sql
RUN echo "CREATE EXTENSION IF NOT EXISTS unaccent;" >> /docker-entrypoint-initdb.d/init.sql
RUN echo "CREATE EXTENSION IF NOT EXISTS btree_gist;" >> /docker-entrypoint-initdb.d/init.sql
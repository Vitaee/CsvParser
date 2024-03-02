FROM python:3.11.8-slim as base

# create the app user
#RUN addgroup -S app && adduser -S app -G app
RUN groupadd -r app && adduser --system app && usermod -a -G app app

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV PYDEVD_DISABLE_FILE_VALIDATION=1
ENV C_FORCE_ROOT true

# Installing temporary packages required for installing requirements.pip 
RUN apt-get update && apt-get install && apt-get install --no-install-recommends -y  \
    gcc \  
    python3-dev \ 
    musl-dev \
    postgresql-server-dev-all\
    zlib1g \
    libjpeg-dev \
    libffi-dev \
    openssl \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN ln -s /usr/lib/x86_64-linux-gnu/libpq.so.5 /usr/lib/x86_64-linux-gnu/libpq.so

# Update pip
RUN pip install --upgrade pip


RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Installing requirements.pip from project
COPY ./src/requirements.txt /scripts/
RUN pip install --no-cache-dir -r /scripts/requirements.txt


# removing temporary packages from docker and removing cache 
RUN apt-get clean && \
    find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip

# Now multistage build
FROM python:3.11.8-slim

# create the appropriate directories
RUN mkdir -p /home/app
ENV HOME=/home/app
ENV APP_HOME=/home/app
WORKDIR $APP_HOME
# Making source and static directory
RUN mkdir $APP_HOME/static


COPY ./src/entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x $APP_HOME/entrypoint.sh



COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /opt/venv /opt/venv

# copy project
COPY ./src .

# RUN apk update && apk add postgresql
ENV PATH=/home/app/.local/bin:$PATH

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install libpq5 binutils libproj-dev gdal-bin python3-gdal libgdal-dev -y


ENV LD_LIBRARY_PATH=/usr/local/lib

# run entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]
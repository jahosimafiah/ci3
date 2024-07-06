ARG PYTHON_VERSION_TAG='3.10-alpine'
FROM python:${PYTHON_VERSION_TAG}

LABEL maintainer='Josiah Allen <josiahallen1980@gmail.com>' 

WORKDIR /tmp/app
COPY . .
RUN \
    pip install . && \
    addgroup -S ci3 && \
    adduser -S ci3 -G ci3 -D

USER ci3
ENTRYPOINT ["ci3"]

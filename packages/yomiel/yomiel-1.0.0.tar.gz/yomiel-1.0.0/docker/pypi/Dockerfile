# -*- coding: utf-8 -*-
#
# jomiel-yomiel
#
# Copyright
#  2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#

# Dockerfile for building a yomiel container from PyPI
#

# builder
#
FROM python:3.8-alpine AS builder

WORKDIR /app

RUN set -eux \
    ; apk --update --no-cache --virtual .build_deps add \
        linux-headers \
        g++ \
    && pip wheel \
        --wheel-dir /app/wheels \
        --no-cache-dir \
        --no-deps \
        yomiel \
        ujson \
        pyzmq \
    && apk del .build_deps

# runtime
#
FROM python:3.8-alpine AS runtime

WORKDIR /app

COPY --from=builder /app/wheels /wheels

RUN set -eux \
    ; apk --update --no-cache add \
        libzmq \
    && pip install --no-cache /wheels/*.whl

ENTRYPOINT ["yomiel"]

CMD ["-h"]

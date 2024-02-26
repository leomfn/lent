# Stage 1: Build frontend assets using npm and webpack
FROM node:21.6-alpine@sha256:f5d3a6aea1b1d35066e6c034f5c264cd5b051fc7c7cb0160bb88899e7b1f0c83 AS assets-builder

WORKDIR /workdir

COPY package.json package-lock.json webpack.config.js ./

RUN npm install

COPY assets ./assets

# ENTRYPOINT [ "/bin/sh" ]

RUN npm run build

# Stage 2: Build Django application

FROM python:3.12-alpine@sha256:849ed6079c9f797ca9c1b7d6aea1c00aea3ac35110cbd0d6003f15950017ea8d AS django-builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY src .

COPY --from=assets-builder /workdir/dist /src/lentapp/static

COPY init.sh /tmp

ENTRYPOINT ["/bin/sh", "/tmp/init.sh"]

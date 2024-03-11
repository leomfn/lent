# Stage 1: Build frontend assets using npm and webpack
FROM node:21.7-alpine@sha256:7bfef1d72befbb72b0894a3e4503edbdc0441058b4d091325143338cbf54cff8 AS assets-builder

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

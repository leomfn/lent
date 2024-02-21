FROM python:3.12-alpine@sha256:849ed6079c9f797ca9c1b7d6aea1c00aea3ac35110cbd0d6003f15950017ea8d

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY src .
COPY init.sh /tmp

ENTRYPOINT ["/bin/sh"]
CMD ["/tmp/init.sh"]

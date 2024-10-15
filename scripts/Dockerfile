FROM advian/pyenv:alpine-3.20

ENV MODULE_NAME=ALL
ENV PYTHON_VERSION=3.13
ENV CPYTHON_SRC=/usr/local/bin/python

COPY . .
RUN pip install -r requirements.txt

CMD [ "python scripts/run_test.py ${MODULE_NAME} ${PYTHON_VERSION}" ]
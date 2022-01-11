FROM python:3.10

# Add a python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# add a regular user
RUN useradd -ms /bin/bash pyuser

# install pylit
COPY pylit-3.1.1 pylit
WORKDIR /pylit
RUN python setup.py install

COPY requirements.txt /requirements/requirements.txt
RUN pip install -r /requirements/requirements.txt

USER pyuser

WORKDIR /home/pyuser/project



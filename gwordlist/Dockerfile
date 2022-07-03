FROM ubuntu
RUN apt update && apt install -y python3 python3-pip
COPY * /gwordlist/
WORKDIR /gwordlist/
RUN pip3 install -r requirements.txt && ln -n /gwordlist/gwordlist.py /usr/bin/gwordlist.py

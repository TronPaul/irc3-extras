FROM micktwomey/python3.4:latest
MAINTAINER Mark Mcguire, mark.b.mcg@gmail.com

RUN pip3.4 install -e git+https://github.com/TronPaul/irc3-extras.git#egg=irc3-extras

from python

# docker build -t felixdu.hz.dynamic.nsn-net.net/sip-proxy -f Dockerfile .

RUN apt-get update && apt-get -y install iproute2

COPY . /tmp/sip-proxy
RUN cd /tmp/sip-proxy && python setup.py install
ENTRYPOINT ["sip-proxy"]

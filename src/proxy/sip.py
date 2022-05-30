class SipMessage():
    def __init__(self, raw_msg):
        self.method = None
        self.status = None
        self.parse(raw_msg)

    def parse(self, msg):
        headers, body = msg.split('\r\n\r\n')
        headers = headers.split('\r\n')

        self.topline = headers[0]
        if self.topline.startswith('SIP/2.0'):
            self.status = self.topline.split(' ', 1)[1]
        else:
            self.method = self.topline.split()[0]

        self.headers = {}
        for x in headers[1:]:
            k, v = x.split(':', 1)
            self.headers.setdefault(k, []).append(v.strip())
        self.body = body

    def insert_header(self, header, value):
        self.headers.setdefault(header, []).insert(0, value)

    def stringify(self):
        msg = f'{self.topline}'
        for k, v in self.headers.items():
            msg += '\r\n' + '\r\n'.join([f'{k}: {x}' for x in v])
        msg += '\r\n\r\n' + self.body
        return msg

if __name__ == '__main__':
    sip_msg = ('INVITE sip:User.0000@tas01.defult.svc.cluster.local SIP/2.0\r\n'
               'Via: SIP/2.0/TCP 0.0.0.0:5060;branch=z9hG4bK-421-1-0\r\n'
               'From: <sip:User.0001@tas01.defult.svc.cluster.local>;tag=1\r\n'
               'To: <sip:User.0000@tas01.defult.svc.cluster.local>\r\n'
               'Call-ID: 1-421@0.0.0.0\r\n'
               'CSeq: 1 INVITE\r\n'
               'Supported: 100rel\r\n'
               'Route: <sip:originating@tafe.default.svc.nokia.local:15306;role=anch;lr;transport=udp;x-suri=sip:scscf-internal.cncs.svc.cluster.local:15090>\r\n'
               'Record-Route: <sip:originating@tafe.default.svc.nokia.local:15306;role=anch;lr;transport=udp;x-suri=sip:pcsf-cfed.cncs.svc.cluster.local:15090>\r\n'
               'Contact: <sip:tafe.default.svc.nokia.local:15306;role=anch;lr;transport=udp;x-suri=sip:pcsf-cfed.cncs.svc.cluster.local:15090>\r\n'
               'P-Asserted-Identity: <sip:User.0001@tas01.defult.svc.cluster.local>\r\n'
               'Allow: UPDATE,INVITE,ACK,CANCEL,BYE,PRACK,REFER,MESSAGE,INFO\r\n'
               'Max-Forwards: 70\r\n'
               'Content-Type: application/sdp\r\n'
               'Content-Length: 123\r\n'
               '\r\n'
               'v=0\r\n'
               'o=PCTEL 256 2 IN IP4 0.0.0.0\r\n'
               'c=IN IP4 0.0.0.0\r\n'
               'm=audio 4030 RTP/AVP 0 8\r\n'
               'a=rtpmap:0 PCMU/8000\r\n'
               'a=rtpmap:8 PCMU/8000)\r\n')
    msg = SipMessage(sip_msg)
    print(msg.stringify())

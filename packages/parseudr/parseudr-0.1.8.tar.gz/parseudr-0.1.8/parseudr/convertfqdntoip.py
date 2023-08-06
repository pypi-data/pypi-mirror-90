import socket


class returnips:

    def tryconvert(fqdn):
        try:
            if fqdn is None:
                return None
            else:
                ipaddr = socket.gethostbyname_ex(fqdn)[2]
                lst = [ip + "/32" for ip in ipaddr]
                return lst
        except:
            pass

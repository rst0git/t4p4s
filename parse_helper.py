#!/usr/bin/env python3

import socket
import sys
import re

HOST = 'localhost'
PORT = int(sys.argv[1])

# To facilitate understanding, almost all named patterns of the regex are separated
patterns = (
    ("cond",      '!condvar(=!condval)?!condsep'),
    ("prefix",    '(\^|:|::|%|%%|@)'),
    ("condvar",   '[a-zA-Z0-9_\-.]+'),
    ("condval",   '[^\s].*'),
    ("condsep",   '(\s*->\s*)'),
    ("letop",     '\+{0,2}='),
    ("letval",    '[^\s].*'),
    ("var",       '[a-zA-Z0-9_\-.]+'),
    ("comment",   '\s*(;.*)?'),
    )

rexp = '^(!prefix|!cond?)?!var(?P<let>\s*!letop?\s*!letval)?!comment$'

# Assemble the full regex
for pattern, replacement in patterns:
    rexp = rexp.replace("!" + pattern, "(?P<{}>{})".format(pattern, replacement))

rexp = re.compile(rexp)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            bline = conn.recv(1024)
            line = bline.decode()
            if line.startswith("exit_parse_helper"):
                sys.exit()

            m = re.match(rexp, line)

            is_ok = 'y' if m else 'n'
            conn.sendall(f'ok {is_ok}\n'.encode())
            for gname in (p[0] for p in patterns):
                opt = '' if not m else m.group(gname) or ''
                conn.sendall(f'{gname} {opt}\n'.encode())
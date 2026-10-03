#!/usr/bin/env python3
"""Explicitly run on the receiver. Captures only; never controls or confirms a boot."""
import argparse
import base64
import json
import socket
import time
import uuid


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bind', required=True, help='Receiver local IPv4 address')
    ap.add_argument('--sender', required=True, help='Expected sender IPv4 address (not authentication)')
    ap.add_argument('--port', type=int, default=6666)
    ap.add_argument('--output', required=True, help='New private JSONL file; never overwrite')
    args = ap.parse_args()
    session = str(uuid.uuid4())
    with open(args.output, 'x', encoding='utf-8', buffering=1) as out, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((args.bind, args.port))
        print('Receiver bound; this is NOT sender qualification. Use one file per boot.', flush=True)
        try:
            while True:
                data, peer = sock.recvfrom(65535)
                if peer[0] != args.sender:
                    continue
                row = {'session': session, 'received_wall_ns': time.time_ns(),
                       'received_monotonic_ns': time.monotonic_ns(),
                       'payload_b64': base64.b64encode(data).decode('ascii')}
                out.write(json.dumps(row) + '\n')
                # Local display only. Exact bytes remain in the private file.
                print(repr(data), flush=True)
        except KeyboardInterrupt:
            print('Capture closed. Completeness is not implied.', flush=True)


if __name__ == '__main__':
    main()

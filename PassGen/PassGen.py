#!/usr/bin/env python3
"""
PassGen.py

Generate N random passwords and write them into ONE output file.

Usage example:
  python3 PassGen.py --count 500000000 --length 12 --outfile passwords.txt --crypto
  python3 PassGen.py --count 500000000 --length 12 --outfile passwords.txt.gz --gzip
"""

import os
import argparse
import string
import gzip

def parse_args():
    p = argparse.ArgumentParser(description='Generate random passwords into one file.')
    p.add_argument('--count', type=int, required=True, help='Total number of passwords to generate (e.g. 500000000)')
    p.add_argument('--length', type=int, default=12, help='Password length (default: 12)')
    p.add_argument('--outfile', type=str, required=True, help='Output file path (e.g. passwords.txt or passwords.txt.gz)')
    p.add_argument('--gzip', action='store_true', help='Compress output with gzip (.gz)')
    p.add_argument('--crypto', action='store_true', help='Use cryptographically secure RNG (secrets)')
    p.add_argument('--charset', type=str, default=None, help='Custom charset (default: all printable password-safe chars)')
    return p.parse_args()

DEFAULT_CHARSET = (
    string.ascii_letters + string.digits +
    "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
)

def main():
    args = parse_args()
    charset = args.charset if args.charset is not None else DEFAULT_CHARSET

    if args.crypto:
        import secrets
        rng_choice = lambda: secrets.choice(charset)
    else:
        import random
        seed = int.from_bytes(os.urandom(8), 'big')
        rng = random.Random(seed)
        rng_choice = lambda: rng.choice(charset)

    make_password = lambda: ''.join(rng_choice() for _ in range(args.length))

    # Choose output mode
    if args.gzip:
        f_open = lambda path: gzip.open(path, 'wt', compresslevel=6)
    else:
        f_open = lambda path: open(path, 'w', buffering=1024*1024)

    total = args.count
    batch_size = 10000  # adjust if you want fewer I/O operations

    print(f"Generating {total} passwords of length {args.length} into {args.outfile}")
    print(f"Charset size: {len(charset)} | Crypto RNG: {args.crypto} | Gzip: {args.gzip}")

    with f_open(args.outfile) as fh:
        written = 0
        while written < total:
            take = min(batch_size, total - written)
            fh.writelines(make_password() + "\n" for _ in range(take))
            written += take
            if written % 1000000 == 0:
                print(f"{written:,} passwords written...")

    print(f"Done! Total written: {total:,} -> {args.outfile}")

if __name__ == '__main__':
    main()

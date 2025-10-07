PassGen.py streams random passwords to disk. Configure total count, password length, character set (alphanumeric / symbols / custom), cryptographic RNG vs. fast PRNG, gzip output, and chunking or single-file output. Designed for large-scale generation with low memory use.

options:
  -h, --help         show this help message and exit
  --count COUNT      Total number of passwords to generate (e.g. 500000000)
  --length LENGTH    Password length (default: 12)
  --outfile OUTFILE  Output file path (e.g. passwords.txt or passwords.txt.gz)
  --gzip             Compress output with gzip (.gz)
  --crypto           Use cryptographically secure RNG (secrets)
  --charset CHARSET  Custom charset (default: all printable password-safe chars)

Usage example:
  python3 PassGen.py --count 500000000 --length 12 --outfile passwords.txt --crypto
  python3 PassGen.py --count 500000000 --length 12 --outfile passwords.txt.gz --gzip

# Hackerolympiad Thomas More & NVISO : Drunkmanshash

**Category:** Programming
**Points:** 50
**Solves:** 1
**Description:** Oh man, I drank way too much beer yesterday. During my not-so-sober state I've changed my password and I can't remember it now. However, I still have the algorithm, hash, and salt. I remember the password was less than 5 characters long and contained only lowercase letters. Can you help me find my plaintext password?

```
PASSWORD = 'Y2FlZDZhMzZlODNlY2M5Mzk5NDUzZGQ3ZmY0MTQ0OTcyZGI2YTgwZGZkYTBiMzU4MDdkMzUyYTNmN2JhMzc5ZDMxMmRjNDU4MDZiMjZmMzA1NzA1MzdlMjA1ZDAzNDc4MmE1M2FmOTNiMTk1ZWU2ODcwOTJhN2JiNTIzMzYwODE='
SALT = '7049548a11ca1d08d017d2429bb04a3b'
```

The used algorithm was: `base64encode( SHA512 * 512( SHA256 * 256( SHA1 ( MD5 * 5( plaintext + salt ) ) ) ) )`

(`SHA512 * 512` means applying SHA512 512 times and all hexdigests are in lowercase)

## Write-up

The password needs to be bruteforced. In order to do this, I wrote a Python script (the password can probably be cracked faster with another language, but Python allows for a rapid dev-cycle).
The cracking speed of this combined hashing algorithm can be improved by first reversing the `base64encode`: since this encodes the information, it is reversible. Running the script took three minutes on my old laptop, so cracking speed isn't that bad. The final Python script for cracking the hash is included in this directory. The password was `frie`.

## Other write-ups and resources

* none yet

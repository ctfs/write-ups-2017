# Ph0wn CTF: Weather station stage 2

**Category**: Reverse, **Points**: 150, **Solves**:

## Description

TODO

## Write-up

The firmware ([WeatherBase.elf](./WeatherBase.elf)) is an ELF
binary compiled for ARM architecture.

With a cross-reference on the string "``Password:``" (string asked by the
binary to enter the administration menu), we find the function that checks
the input password.

```
[0x0800f520]> iz~Password:
vaddr=0x08015a64 paddr=0x00025a64 ordinal=104 sz=11 len=10 section=.rodata
type=ascii string=Password: 
[0x08015a64]> axt 0x08015a64
(nofunc) 0x800d6ec [null] ldrh r4, [r4, r1] 
[0x08015a64]> axt 0x800d6ec
fcn.0800d5d8 0x800d5dc [data] ldr r2, [0x0800d6ec]
```

This function is located at *0x0800d5d8*. Via a static analyse, we
understand that each password character 'p' must verifies the expression
*(a XOR p) - k = 0*, with:

- *a*: a character from the string "W362T7uC"
- *k*: equal to 3 or 7 depending on the byte parity of characters from the
  string "SuperSec"

We deduce: *p = (a XOR k)*.

The following script recover the password:

```python
#!/usr/bin/python3

a="W362T7uC"
b="SuperSec"
p = ""

for i in range(0,8):
    if ((ord(b[i])) & 1):
        k = 7
    else:
        k = 3

    p += chr((ord(a[i]) ) ^ k)

print("The password is: {}".format(p))
```

The password is "**P455W0rD**". We had to connect to the real Weather
station with Minicom (and the good baud rate, see stage 1) to display the
flag.

## Other write-ups and resources

[SEC-IT](https://blog.sec-it-solutions.fr/write-up/2017/12/05/jla-writeup-ph0wn-1.html)


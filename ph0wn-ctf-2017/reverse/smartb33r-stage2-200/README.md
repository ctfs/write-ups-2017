# Ph0wn CTF: Smart B33r - Stage 2

**Category**: Hardware, **Points**: 200, **Solves**: 1

## Description

Did you get stage 1 flag? Well done.
Or not? And you want to start the hard way? Up to you!

There's a second flag to find on our Arduino board.
Good luck.

Please come and book a time slot for the board.

Update: To solve this challenge, you need to solve Smart B33r 1 first!

Author: Tony Beer


## Write-up

The dump of the flash that you got during stage 1 is [here](./flash.raw)

### Balda's solution

With the firmware available, we can start to analyze the firmware. Let's run
radare2 :

```
r2 -a avr /tmp/flash
[0x000000c4]> afr
[0x000000c4]> pd 17
            ;-- entry0:
            ;-- pcl:
            0x000000c4      1124           clr r1
            0x000000c6      1fbe           out 0x3f, r1
            0x000000c8      cfef           ser r28
            0x000000ca      d8e0           ldi r29, 0x08
            0x000000cc      debf           out 0x3e, r29
            0x000000ce      cdbf           out 0x3d, r28
            0x000000d0      12e0           ldi r17, 0x02
            0x000000d2      a0e0           ldi r26, 0x00
            0x000000d4      b1e0           ldi r27, 0x01
            0x000000d6      eae8           ldi r30, 0x8a
            0x000000d8      fee0           ldi r31, 0x0e
        ┌─< 0x000000da      02c0           rjmp 0xe0
       ┌──> 0x000000dc      0590           lpm r0, z+
       ││   0x000000de      0d92           st x+, r0
       │└─> 0x000000e0      a835           cpi r26, 0x58
       │    0x000000e2      b107           cpc r27, r17
       └──< 0x000000e4      d9f7           brne 0xdc
```
This first part is often seen at the beginning of AVR firmwares, and copies data
from the flash memory to the RAM (since those are separate memory spaces in
AVR). In this case, `0x158` bytes are copied from `0xe8a` in flash to `0x100` in RAM.

To see the data to be copied, we can issue the following command :

```
[0x000000c4]> px 0x158 @ 0xe8a
- offset -   0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x00000e8a  5374 6167 6531 2066 6c61 673a 2070 6830  Stage1 flag: ph0
0x00000e9a  776e 7b57 6548 6f70 6559 6f75 4c69 6b65  wn{WeHopeYouLike
0x00000eaa  4156 527d 0070 6830 776e 4172 6475 696e  AVR}.ph0wnArduin
0x00000eba  6f00 0000 0000 1f01 8c00 b700 6601 e800  o...........f...
0x00000eca  c600 da00 0000 0000 c404 0d0a 0050 6830  .............Ph0
0x00000eda  776e 2041 7264 7569 6e6f 2063 6861 6c6c  wn Arduino chall
0x00000eea  656e 6765 2076 312e 3300 4174 7465 6d70  enge v1.3.Attemp
0x00000efa  7469 6e67 2074 6f20 636f 6e6e 6563 7420  ting to connect 
0x00000f0a  746f 2057 5041 3220 7769 6669 2077 6974  to WPA2 wifi wit
0x00000f1a  6820 7374 6167 6531 2070 6173 732e 2e2e  h stage1 pass...
0x00000f2a  0053 7461 6765 2032 3a20 6669 6e64 2074  .Stage 2: find t
0x00000f3a  6865 206f 7468 6572 2066 6c61 6721 005b  he other flag!.[
0x00000f4a  2d5d 2041 7474 656d 7074 696e 6720 746f  -] Attempting to
0x00000f5a  2063 6f6e 6e65 6374 2077 6974 6820 7374   connect with st
0x00000f6a  6167 6532 2070 6173 732e 2e2e 005b 2d5d  age2 pass....[-]
0x00000f7a  204e 6f74 2063 6f6e 6e65 6374 6564 2074   Not connected t
0x00000f8a  6f20 7769 6669 005b 2b5d 2043 6f6e 6e65  o wifi.[+] Conne
0x00000f9a  6374 6564 2074 6f20 7769 6669 2077 6974  cted to wifi wit
0x00000faa  6820 7374 6167 6520 3220 7061 7373 005b  h stage 2 pass.[
0x00000fba  2b5d 2043 6f6e 6e65 6374 6564 2074 6f20  +] Connected to 
0x00000fca  7769 6669 2077 6974 6820 7374 6167 6520  wifi with stage 
0x00000fda  3120 7061 7373 0000                      1 pass..
```
Now that we know about this behavior, we can copy this data in a separate memory
space in r2. For that, we enable the IO cache (to write in memory), create a RAM
section in a new memory space (`0x080000`) and copy data into it.

```
[0x000000c4]> e io.cache=true
[0x000000c4]> S 0x080000 0x080000 0x1000 ram
[0x000000c4]> wd 0x0xe8a 0x158 @ 0x080000
```

Since we now have the RAM correctly initialized, we can dig deeper in the
firmware and see what it does.

Once the RAM is loaded, the function at `0xc32` is called. Looking at the code,
we can see several calls to the same function `fcn.0000076a` :

```
0x00000d36      6de4           ldi r22, 0x4d
0x00000d38      71e0           ldi r23, 0x01
0x00000d3a      8be6           ldi r24, 0x6b
0x00000d3c      92e0           ldi r25, 0x02
0x00000d3e      0e94b503       call fcn.0000076a
0x00000d42      6ae6           ldi r22, 0x6a
0x00000d44      71e0           ldi r23, 0x01
0x00000d46      8be6           ldi r24, 0x6b
0x00000d48      92e0           ldi r25, 0x02
0x00000d4a      0e94b503       call fcn.0000076a
0x00000d4e      80e0           ldi r24, 0x00
0x00000d50      91e0           ldi r25, 0x01
0x00000d52      0e94c903       call fcn.00000792
0x00000d56      90936302       sts 0x263, r25
0x00000d5a      80936202       sts 0x262, r24
0x00000d5e      0397           sbiw r24, 0x03
0x00000d60      09f4           brne 0xd64
0x00000d62      5bc0           rjmp 0xe1a
0x00000d64      61ea           ldi r22, 0xa1
0x00000d66      71e0           ldi r23, 0x01
0x00000d68      8be6           ldi r24, 0x6b
0x00000d6a      92e0           ldi r25, 0x02
0x00000d6c      0e94b503       call fcn.0000076a
0x00000d70      6feb           ldi r22, 0xbf
0x00000d72      71e0           ldi r23, 0x01
0x00000d74      8be6           ldi r24, 0x6b
0x00000d76      92e0           ldi r25, 0x02
0x00000d78      0e94b503       call fcn.0000076a
```

If we take a look at the arguments passed to this function, we can see a fixed
value of `0x26b` in registers `r24:r25` and a different value in registers
`r22:r23`. Looking at its content, we can see that it's a pointer to a string to
be printed :
```
[0x00000c32]> ps @ 0x080000+0x14d
Ph0wn Arduino challenge v1.3
```
Same goes for all subsequent calls, so we can rename this function as print_str
:
```
[0x000000c4]> afn print_str 0x76a
```

We then have a call to `fcn.00000792` with a pointer to `0x100`. Let's see :

```
[0x00000c32]> ps @ 0x080000+0x100
Stage1 flag: ph0wn{WeHopeYouLikeAVR}
```

So this function could be the stage pass function. We can see if there is a
second call to this function like this :
```
[0x00000c32]> axt @ fcn.00000792
fcn.00000c32 0xd52 [call] call fcn.00000792
fcn.00000c32 0xdf6 [call] call fcn.00000792
```

This function is called after a bunch of load/store instructions between `0xd7c`
and `0xdf6` maybe the second flag is computed here.

I didn't find a way to use r2's ESIL emulation to generate the flag, but here
is a poor man's emulator in python :

```
import re
s="""ldi r24, 0x70
std y+1, r24
ldi r24, 0x68
std y+2, r24
ldi r25, 0x30
std y+3, r25
ldi r24, 0x77
std y+4, r24
ldi r24, 0x6e
std y+5, r24
ldi r24, 0x7b
std y+6, r24
ldi r24, 0x38
std y+7, r24
ldi r19, 0x63
std y+8, r19
ldi r21, 0x31
std y+9, r21
ldi r18, 0x34
std y+10, r18
ldi r18, 0x64
std y+11, r18
std y+12, r24
ldi r18, 0x37
std y+13, r18
ldi r24, 0x36
std y+14, r24
ldi r20, 0x39
std y+15, r20
std y+16, r25
std y+17, r18
std y+18, r18
ldi r22, 0x35
std y+19, r22
std y+20, r20
ldi r24, 0x65
std y+21, r24
std y+22, r18
std y+23, r25
std y+24, r22
ldi r18, 0x62
std y+25, r18
std y+26, r20
ldi r18, 0x66
std y+27, r18
std y+28, r25
std y+29, r24
std y+30, r25
std y+31, r24
ldi r25, 0x61
std y+32, r25
std y+33, r19
std y+34, r18
std y+35, r19
std y+36, r24
std y+37, r21
std y+38, r24
ldi r24, 0x7d
std y+39, r24
"""

r = re.compile("(\S+) (\S+), (\S+)")

flag = list('\x00'*255)

for i in s.split('\n'):
    print i
    instr, op1, op2 = r.match(i).groups()
    if instr=='ldi':
        vars().update({op1:int(op2[2:], 16)})
    if instr == 'std':
        offset = int(op1.split('+')[1])
        flag[offset] = chr(vars()[op2])

print ''.join(flag)
```
And this prints the flag : 
```
ph0wn{8c14d876907759e705b9f0e0eacfce1e}
```

> Note : It was also possible to use simavr and get the same result by breaking
> at address 0xdf6 and printint the memory contents. around 0x100 to get the flag.


## Write-ups and resources on  other websites



# Ph0wn CTF: Smart B33r - Stage 1

**Category**: Hardware, **Points**: 100, **Solves**: 5

## Description

This morning, our management came up with a great idea. Yes, for once, it was really a great idea: a **smart draught beer-tapping machine!**

We decided to implement it right away, and you'll be working on our Arduino prototype. Come and get one, and see if you get closer to b33r.

Nota. Oops, we forgot to set up the wifi.

Update: To solve this challenge, you need to find a way to extract the device's firmware!

Rules:

-  Book a time slot to get the Arduino prototype
-  Please do not physically destroy our prototype.

Author: Tony Beer


## Write-up

We dump code from the Arduino, using `avrdude`. This program can be found in the
 arduino package in `ARDUINO_INSTALL_PATH/hardware/tools/avr/bin`.

`avrdude -p partno -P port -c programmer -C configfile -U memtype:op:filename:fo
rmat`

- partno: what type of MCU is connected to the programmer. [We have an Arduino U
no R3](https://store.arduino.cc/arduino-uno-rev3). This is using the microcontro
ller ATmega328p.  So part number must be `m328p` (see [avrdude options](http://w
ww.nongnu.org/avrdude/user-manual/avrdude_4.html#Option-Descriptions)).

- programmer: `arduino` in our case

- config file: to be found in `ARDUINO_INSTALL_PATH/hardware/tools/avr/etc/avrdu
de.conf`

- port: `/dev/ttyACM0` in my case

- memory operation: we will read the flash of the device so memtype is `flash`.

The operatio is read: `r`. Then we specify the filename to dump to. Finally the 
format can be for example `i` for Intel Hex.

Note: there are path issues if you invoke `avrdude` outside `ARDUINO_INSTALL_PAT
H/hardware/tools/avr/bin`. So, go to that directory first.

### Dumping in raw (easier)

```bash
$ cd ~/softs/arduino-1.8.5/hardware/tools/avr/bin
$ ./avrdude -p m328p -P /dev/ttyACM0 -c arduino -C ../etc/avrdude.conf -U flash:
r:flash.raw:r
...
avrdude: writing output file "challenge.raw"

avrdude: safemode: hfuse reads as 0
avrdude: safemode: efuse reads as 0
avrdude: safemode: Fuses OK (E:00, H:00, L:00)

avrdude done.  Thank you.
```

You might need to `sudo`. Then, do:

```bash
$ strings flash.raw 
!P1	
OB.Q,a,q,
#+$+%+a
O__O
O__O
Stage1 flag: ph0wn{WeHopeYouLikeAVR}
ph0wnArduino
Ph0wn Arduino challenge v1.2
Attempting to connect to WPA2 wifi with stage1 pass...
[-] Attempting to connect with stage2 pass...
[-] Not connected to wifi
[+] Connected to wifi with stage 2 pass
[+] Connected to wifi with stage 1 pass
$N__O
```

So, the first flag is `ph0wn{WeHopeYouLikeAVR}`

### Dumping in Intel Hex mode (longer)

```bash
$ cd ~/softs/arduino-1.8.5/hardware/tools/avr/bin
$ ./avrdude -p m328p -P /dev/ttyACM0 -v -c arduino -C ../etc/avrdude.conf -U fla
sh:r:challenge.ihex:i

avrdude: Version 6.2
...
avrdude: writing output file "challenge.ihex"

avrdude: safemode: hfuse reads as 0
avrdude: safemode: efuse reads as 0
avrdude: safemode: Fuses OK (E:00, H:00, L:00)

avrdude done.  Thank you.
```

Then, you need to convert the file to binary format. For that, there is an Intel  hex python package: `sudo pip install bincopy`.
Then, convert with this small script:

```python
import bincopy
import sys

f = bincopy.BinFile()
f.add_ihex_file(sys.argv[1])
print(f.as_binary())
```



## Other write-ups and resources

### Using Hydrabus (Balda)

Connecting to the device, we are greeted with this message :

```
Ph0wn Arduino challenge v1.3

Attempting to connect to WPA2 wifi with stage1 pass...
Stage 2: find the other flag!
[-] Attempting to connect with stage2 pass...
[-] Not connected to wifi
```

A hint on the challenge description tells us that we need to dump the firmware
to get the flag. Let's go.

I took my Hydrabus and connected its SPI2 interface on the ICSP connector of the
arduino board.

|ICSP|Hydrabus|Function|
|----|--------|--------|
| 1  | PC2    | MISO   |
| 2  | 3.3v   | 3.3v   |
| 3  | PB10   | SCK    |
| 4  | PC3    | MOSI   |
| 5  | PC1    | CS     |
| 6  | GND    | GND    |

Once connected, we just need to run the following command to dump the firmware
:
```
avrdude -v -v -v -p m328p -c buspirate -P /dev/hydrabus -U flash:r:/tmp/flash:r
```

Once completed, running `strings /tmp/flash` shows the first flag :

```
$ strings /tmp/flash
 [...]
Stage1 flag: ph0wn{WeHopeYouLikeAVR}
 [...]
```
>  Note : After discussing with the challenge author, the intended way to solve
>  this was to simply dump the firmware using DFU, so no extra hardware was
>  needed.


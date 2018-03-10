# Ph0wn CTF: Weather station stage 1

**Category**: Reverse, **Points**: 50, **Solves**: 11

## Description

You've just unboxed this nice weather station, will you manage to connect it to a computer and interact with it?

To score this challenge please enter a flag in the form of 'Ph0wn{xxxxx}'.

Come and book the weather station at the admin desk.


Author: Phil


## Write-up

The weather station is made of an STM Nucleo board, and a custom daughterboard. Let's power it and have a look at what `dmesg` says:

```
[17495.098051] usb 2-1.7: Manufacturer: STMicroelectronics
[17495.098052] usb 2-1.7: SerialNumber: 0674FF575450707267222256
[17495.186979] cdc_acm 2-1.7:1.2: ttyACM0: USB ACM device
```

Plug also the FTDI USB:

```
[18799.785521] usb 1-1.3: Product: USB <-> Serial Cable
[18799.785521] usb 1-1.3: Manufacturer: FTDI
[18799.785522] usb 1-1.3: SerialNumber: 12345678
[18800.815385] usbserial: USB Serial support registered for FTDI USB Serial Device
[18800.815454] ftdi_sio 1-1.3:1.0: FTDI USB Serial Device converter detected
[18800.815515] usb 1-1.3: Detected FT232RL
...
[19117.241233] ftdi_sio ttyUSB0: FTDI USB Serial Device converter now disconnected from ttyUSB0
...
[19129.657995] usb 1-1.3: FTDI USB Serial Device converter now attached to ttyUSB0
```

So, the USB is on `/dev/ttyUSB0`.

We use `microcom` to communicate with the board:

```
$ sudo microcom -d -s 9600 -p /dev/ttyUSB0
connected to /dev/ttyUSB0
Escape character: Ctrl-\
Type the escape character followed by c to get to the menu or q to quit
Ã¯Â¿Â½Ã¯Â¿Â½Ã¦
```

Damn! What's that garbage! We try another speed.

```
sudo microcom -d -s 19200 -p /dev/ttyUSB0
connected to /dev/ttyUSB0
Escape character: Ctrl-\
Type the escape character followed by c to get to the menu or q to quit


Check for hardware probe ...
Not found, skip I2C sending

Hardware initialization...
Stack @ 0x20017fe4
Weather Station OS V1.02 beta 3 started
Station is ready to run.
flag50 is Ph0wn{Seri@l port always matter!}



Password:
```

There we go for the first flag: `Ph0wn{Seri@l port always matter!}`


## Other write-ups and resources

TODO


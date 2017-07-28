# Hackerolympiad Thomas More & NVISO : Is it trying to tell me something?

**Category:** Cryptography
**Points:** 15
**Solves:** 2
**Description:** Find the flag in the BSOD.scr file. You can find it between quotes.



## Write-up

This was a steno challenge categorized as a crypto challenge. As usual with steno challenges, I executed the `file` command:
```
$: file BSOD.scr
BSOD.scr: Zip archive data, at least v2.0 to extract
```
I then unzipped the file (`unzip BSOD.scr`), this resulted in 6 PNG files named `BSOD1.png` trough `BSOD6.png`. When I saw these pictures in an image viewer, they all looked like this: a blue background and white characters spread over the screen.
![BSOD1.png](BSOD1.png)
I then opened these images as separated layers in GIMP and removed the blue background of every layer except the last one. This was the result:
![Solution](BSOD_solution.png)
The flag was: `The user is going to pick dancing pigs over security every time`.

## Other write-ups and resources

* none yet

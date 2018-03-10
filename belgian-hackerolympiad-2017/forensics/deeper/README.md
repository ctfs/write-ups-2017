# Hackerolympiad Thomas More & NVISO : Deeper

**Category:** Forensics
**Points:** 100
**Solves:** 2
**Description:** It's my birthday tomorrow, my collegues are getting me a gift. I asked them for a hint and they gave me this data.pcap file, but I have no clue what this is. Can you help me find what they bought me?

## Write-up

The PCAP contained some HTTP packets, so I set a filter: `http`. In one of the packets was a pastebin link: https://pastebin.com/iSy0jvLE. The paste was some base64 encoded text, so I decoded it with [CyberChef](https://gchq.github.io/CyberChef/#recipe=%5B%7B%22op%22%3A%22From%20Base64%22%2C%22args%22%3A%5B%22A-Za-z0-9%2B%2F%3D%22%2Ctrue%5D%7D%5D&input=Wm14aFp6b2dUV0YwY25sdmMyaHJZUT09). This resulted in `flag: Matryoshka`. The flag was `Matryoshka`.

## Other write-ups and resources

* none yet

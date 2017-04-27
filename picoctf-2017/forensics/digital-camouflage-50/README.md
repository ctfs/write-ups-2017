# picoCTF 2017 : digital-camouflage-50

**Category:** Forensics
**Points:** 50
**Solves:**
**Description:**

> Find the location of the flag in the image: image.jpg. Note: Latitude and longitude values are in degrees with no degree symbols,/direction letters, minutes, seconds, or periods. They should only be digits. The flag is not just a set of coordinates - if you think that, keep looking!
>
>  HINTS
>
> How can images store location data? Perhaps search for GPS info on photos.

## Write-up

A quick bit of Googling reveals that `.pcap` files are **Packet Captures** which contain the transmissions between hosts across a network. For organized viewing, opening in Wireshark (or CloudShark online with free trial) you can peruse through the packets. Nearly every router communicates with a system administrator (the user in charge of configuring the router) using a web interface. All major web transmissions are done through HTTP requests (GET, POST, PUT, DELETE, etc.). Therefore we want to look at all requests labeled `HTTP`, as one of them will likely contain the transmission. A quick search through the PCAP reveals there are only 9 HTTP packets.

With even more knowledge, you might know that login and authentication processes utilize the POST request, sending the authentication information (e.g. username and/or password) in the content of the request. Looking then at all HTTP requests with the POST method (only one!), we look a few lines down and see the payload of the POST request: `userid=spiveyp&pswrd=S04xWjZQWFZ5OQ%3D%3D` which looks exactly like a login. The password contents (`S04xWjZQWFZ5OQ%3D%3D`) appears to be HTML encoded (as all POST data sent over HTTP needs to be) as you can tell by the repeated `%` characters.

Using [this site](http://www.asciitohex.com/), you can paste the password into the **URL Encoded** box, click **Convert** and see revealed in the ASCII box: `S04xWjZQWFZ5OQ==`. Doesn't look like a password, however any string ending with double equal signs usually indicates the string is encoded using Base64.

Copying the last result into the **Base64** box on the same page and clicking **Convert** will leave you with the string `KN1Z6PXVy9` in the ASCII box. That looks more like a password (and a decent password at that). Paste that into the flag submission box for 50 points.

*For the less organized (or lazy) just open a text or hex editor and search for `POST` and it'll bring you right there.*
## Other write-ups and resources

* none yet

# picoCTF 2017 : special-agent-user-50

**Category:** Forensics
**Points:** 50
**Solves:**
**Description:**

> We can get into the Administrator's computer with a browser exploit. But first, we need to figure out what browser they're using. Perhaps this information is located in a network packet capture we took: data.pcap. Enter the browser and version as "BrowserName BrowserVersion". NOTE: We're just looking for up to 3 levels of subversions for the browser version (ie. Version 1.2.3 for Version 1.2.3.4) and ignore any 0th subversions (ie. 1.2 for 1.2.0)
>
>  HINTS
>
> Where can we find information on the browser in networking data? Maybe try reading up on user-agent strings.

## Write-up

If you look at the hint, it suggests researching into **User-Agent** strings. In short, these strings are sent from your browser to a website when you access that website which tells the server what browser you are using so it can better format what it sends back for webpages. This `PCAP` file (packet capture) can be opened in a packet viewing software (Wireshark), a hex editor, or even a text edit. The file has quite a few HTTP requests in them, each carrying an **User-Agent** header. Six of them are `Wget/1.16 (linux-gnu)`, but Googling "wget" reveals that it is not a browser, but a Linux command line tool for fetching webpages. However, one of the HTTP requests contains the string `User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F`. The first 4/5 of the string contain information about components of the browser, however you should see two familiar names, **Chrome** and **Safari**. Chrome is the only one with a version number, and the description states only the first 3 levels of subversions are needed so the flag is `Chrome 34.0.1847`.

## Other write-ups and resources

* none yet

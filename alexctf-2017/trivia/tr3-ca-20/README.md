# AlexCTF: TR3: CA

**Category:** Trivia
**Points:** 20
**Solves:** 719
**Description:**

> What is the CA that issued Alexctf https certificate
>
> (flag is lowercase with no spaces)

## Write-up

A quick Google query on the term `CA` with regards to HTTPS certificates should provide a basic understanding the role of a CA (Certificate Authority) in SSL certificates. Because the CA is the organization that issues these certificates to the website, clients can view information regarding the who issued the certificate and who it was issued to.

### Firefox

To view the certificate information with Firefox:
  1. While on the CTF's website, click on the green lock in the URL bar of the browser
  2. Click the right facing arrow next to the site name
  3. The CA's name appears under the `Verified by` header

### Chrome

To view the certificate information with Chrome:
  1. While on the CTF's website, right click on the webpage
  2. Select **Inspect Element**
  3. Click on the **Security** tab
  4. Click on **View Certificate**
  5. The CA's name is listed next to the `Issued to` header

### Edge

To view the certificate information with Edge click on the green lock and the CA's name is shown as _NAME has identified this site as..._

## Other write-ups and resources

 * [Rawsec](http://rawsec.ml/en/AlexCTF-2017-write-ups/#30-TR3-CA-Trivia)
 * [R3dCr3sc3nt](https://github.com/R3dCr3sc3nt/AlexCTF/blob/master/TR3-CA/README.md)

# AlexCTF: TR4: Doesn't our logo look cool ?

**Category:** Trivia
**Points:** 40
**Solves:** 531
**Description:**

(No description)

## Write-up

After copy and pasting the ALEXCTF logo into a file `logo`, it's easy to observe that it includes a lot of whitespace. So to get ride of the whitespace:  
`cat logo | tr -d [:space:]`  

and we see that while the file is much smaller, it includes a bunch of odd characters with some letters sprinkled around. We can carefully build up an expression with `sed` that will replace the weird characters with nothing:  
```cat logo | tr -d [:space:] | sed s/[@\'\`+\.:#\;,]//g```
* the syntax is s/string-to-replace/string-to-replace-with/
* the ending `g` means "global" since it's all one line
* the `[]` means to find any of the characters inside (e.g. `@` or `'` instead of both in a row)
* note that some characters need to be escaped: ``` ' . ; ` ```

and our flag is:  
`ALEXCTF{0UR_L0G0_R0CKS}`

## Other write-ups and resources

 * http://rawsec.ml/en/AlexCTF-2017-write-ups/#40-TR4-Doesn%E2%80%99t-our-logo-look-cool-Trivia
 * https://pwnable.io/alexctf-tr4-doesnt-logo-look-cool-write/
 * https://blog.passwd.ninja/index.php/2017/02/05/alexctf-2017-logo/
 * https://github.com/ChalmersCTF/Writeups/tree/master/AlexCTF%202017-02-05/tr4
 * https://www.youtube.com/watch?v=zczOyaXxGpQ
 * https://github.com/R3dCr3sc3nt/AlexCTF/blob/master/TR4-Doesnt_our_logo_look_cool/README.md

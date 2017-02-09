# Break In 2017 - Aalekh and a secret window


**Category:** Networking
**Points:** 100
**Solves:** (TODO)
**Description:**

> We all know that Felicity is coming and Aalekh is very busy in making the questions for breakin. During the same time, Animesh came to know a secret regarding Aalekh.
> He found that Aalekh had recently started liking a girl, but they do not talk in a usual way. Animesh know that Aalekh is very secretive and he will not share her name easily.
> Hence he asked Aalekh to give him a hint so that Animesh can figure out her name himself. On Animesh's request, Aalekh made a find the flag challenge, and gave him the hint that there is a secret window in their hostel which Aalekh uses to communicate with her.
> Animesh knows that all the windows in the hostel are assigned some numbers and Aalekh had stored the hash of the number corresponding to that secret window.
> Mandy, a common friend of Aalekh and Animesh had somehow managed to get the md5 hash sum of that window number, which is 208e43f0e45c4c78cafadb83d2888cb6. Now Animesh and Mandy wonders how they can solve Aalekh's challenge so that they can know the name of that unknown person!

> Can you help them?

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

When you crack the given md5 (which is easy to crack as it's given that it is a md5sum corresponding to a number), you get the number to be 1143.
Now the question gives one more hint that all the windows in the hostel are assigned some numbers, which can be related to the port numbers.

Also it was given that Aalekh and that girl do NOT talk in a usual way, which gives us the hint that some other protocol (instead of usual TCP) is involved.

On sending a test UDP request on port 1143 of [https://felicity.iiit.ac.in](https://felicity.iiit.ac.in), we get the response as:
```bash
printf "hello" | nc -u felicity.iiit.ac.in 1143
# => bad method
```
Which suggests us to change the method of the request.

When we change the method to PUT we obtain this:
```bash
printf "PUT / HTTP/1.0\r\n" | nc -u felicity.iiit.ac.in 1143
# => Header-Missing: i-want-flag
```

Now if we include the header `i-want-flag` and set it's value to be `true` (or anything other than `false`), we get the response:
```bash
printf "PUT / HTTP/1.0\r\ni-want-flag: true\r\n" | nc -u felicity.iiit.ac.in 1143
# Only a person who wanted to find the flag - find it, but not use it - would be able to get it.
```
Now solve this little riddle and set the value for i-want-flag to be `false`, and you are good to go.
```bash
printf "PUT / HTTP/1.0\r\ni-want-flag: false\r\n" | nc -u felicity.iiit.ac.in 1143
# => flag: felicityissometimesfun
```

Clearly the flag is `felicityissometimesfun`

## Other write-ups and resources
* none yet
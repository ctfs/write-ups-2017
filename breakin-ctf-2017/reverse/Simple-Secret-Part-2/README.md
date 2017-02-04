# Break In 2017 - Simple Secret - Part 2


**Category:** Reverse
**Points:** 100
**Solves:** (TODO)
**Description:**

> As Aalekh successfully cracked the secret given by Mandy in Simple Secret- Part 1 Mandy comes with a stronger way of hiding the secret.
> Can you help Aalekh this time? 

> Link to executable: [here](https://goo.gl/vbL4Ah)

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

Download the given executable and try `ltrace ./a.out` (after giving proper executable permissions to the given a.out). The output is something like this:

![Ltrace log](https://cloud.githubusercontent.com/assets/9266422/22549459/74297aea-e971-11e6-8ca9-76f76be70b4b.png)

Clearly you can see a URL being constructed from parts, which as a whole looks like
`54.175.180.76/api/breakin/?string=<a_random_20_characters_string>`
Just open this url and you get the response as `the_flag_is_c47aced5c6004d6c868fffd74dc6f61b`

Clearly the flag is `c47aced5c6004d6c868fffd74dc6f61b`

## Other write-ups and resources
* https://github.com/pogTeam/writeups/tree/master/2017/BreakIn/Simple%20Secret%20-%20Part%202
* https://advancedpersistentjest.com/2017/01/30/writeup-simple-secret-2-break-in-ctf-grgsm_livemon-headless-mode/
* https://www.youtube.com/watch?v=3xZUxjVuKOo
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/simple_secret_part_2

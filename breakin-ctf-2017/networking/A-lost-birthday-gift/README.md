# Break In 2017 - A lost birthday gift


**Category:** Networking
**Points:** 100
**Solves:** (TODO)
**Description:**

> The birthday party of Saumya had already started (without inviting Animesh), but Animesh is not upset regarding this.
> Instead, he bought a birthday gift for her (obviously with a hidden flag) and thought of gifting it to Saumya.
> Unfortunately on his way to the venue of birthday party, he accidentally dropped the gift in a heap of sand.
> The party is going to end very soon and Animesh wish to gift her before the party is over. For that, he is trying very hard to dig every place in search of his gift. 

> Can you help him in finding the lost gift?

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

The problem statement may look weird as it does not provide and external file, link etc. However, when if you observe the last line of the problem, you find the statement _he is trying very hard to dig every place in search of his gift_ which gives you the hint to use "dig" command to reach to the solution. But again the problem is, we don't know where to dig. For this a hint was given during the contest: _The link is here only, you need to have the sight of a hacker to get it_, which suggests you to dig on the contest domain ([felicity.iiit.ac.in](https://felicity.iiit.ac.in)). 

Now for reaching the desired output, when you try to dig at [felicity.iiit.ac.in](https://felicity.iiit.ac.in) using the domain as the nameserver, you get the response
```bash
dig any felicity.iiit.ac.in @felicity.iiit.ac.in +short
# => "yougotit=the_flag_is_240bc306d1a19916d636f3d614e03024"
```

Clearly the flag is `240bc306d1a19916d636f3d614e03024`
## Other write-ups and resources
* https://github.com/USCGA/writeups/blob/master/online_ctfs/breakin_2017/a_lost_birthday_gift/

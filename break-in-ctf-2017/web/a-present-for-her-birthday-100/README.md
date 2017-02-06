# Break In CTF 2017 : a-present-for-her-birthday-100

**Category:** Web
**Points:** 100
**Solves:** 
**Description:**

Yesterday was Animesh's best friend's (at least he thinks so) birthday. Animesh had bought a nice present for her, but she didn't even invite Animesh :-( . He came to know that only the people who have the secret key for the birthday party can get the invitation the party. Unfortunately Animesh does not have that key, but he know that the key can be found [here](https://felicity.iiit.ac.in/contest/extra/birthday/). Can you help Animesh find the key so that he can attend her birthday party and give her the sweetest present he bought for her.

## Write-up

When we visit the linked page we are presented with:

	Sorry You are not allowed to visit this page.

as there is nothing else to see, we take a look at the cookie:

	birthday_invite=68934a3e9455fa72420237eb05902327

Throwing this into python we get:

	>>>cookie = "68934a3e9455fa72420237eb05902327"
	>>>cookie.decode("hex")
	"h\x93J>\x94U\xfarB\x027\xeb\x05\x90#'"

Which doesn't get us any further. However, the cookie has the same
length as a MD5 hash, so let's try to crack. You can use you favorite online
MD5-database for that:

	68934a3e9455fa72420237eb05902327 -> md5(false)

So let's try to set our cookie to "true":

	$ echo -n true | md5sum
	b326b5062b2f0e69046810717534cb09

Setting the cookie to this value and visiting the page again we see:

	the_flag_is_6bdfde3455a864cde19362cc01da125f

The flag is: the_flag_is_6bdfde3455a864cde19362cc01da125f

## Other write-ups and resources

* https://github.com/pogTeam/writeups/tree/master/2017/BreakIn/A%20present%20for%20her%20Birthday
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/a_present_for_her_birthday
* https://www.youtube.com/watch?v=uIfjNOZmvzs

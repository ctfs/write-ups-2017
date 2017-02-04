# Break In 2017 - A present for her Birthday!


**Category:** Web
**Points:** 100
**Solves:** (TODO)
**Description:**

> Yesterday was Animesh's best friend's (at least he thinks so) birthday. Animesh had bought a nice present for her, but she didn't even invite Animesh :-(
> He came to know that only the people who have the secret key for the birthday party can get the invitation to the party. 
> Unfortunately Animesh does not have that key, but he know that the key can be found [here](https://felicity.iiit.ac.in/contest/extra/birthday/).
> Can you help Animesh find the key so that he can attend her birthday party and give her the sweetest present he bought for her.


## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

When you go to the given link, the page says `Sorry you are not allowed to visit this page`. On having a look at the cookies, you see a cookie by the name "birthday_invite", whose value was set as some md5sum. When you paste the given md5 on any online rainbow tables, you find the result to be `false` 
Change the cookie corresponding to "birthday_invite" to be the md5sum of `true`, and refresh the page. You see the response as `the_flag_is_6bdfde3455a864cde19362cc01da125f`

Clearly the flag is `6bdfde3455a864cde19362cc01da125f`

## Other write-ups and resources
* https://github.com/pogTeam/writeups/tree/master/2017/BreakIn/A%20present%20for%20her%20Birthday!
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/a_present_for_her_birthday
* https://www.youtube.com/watch?v=uIfjNOZmvzs

# Break In CTF 2017 : fast-and-furious-100

**Category:** Web
**Points:** 100
**Solves:** 
**Description:**

Animesh and Aalekh are very good friends. Animesh always like things working at Ultra fast speed and gave Aalekh a challenging task. He asks Aalekh to complete the task, after the completion of which, Animesh will give Aalekh a Juice Treat. Can you help Aalekh getting a Juice Treat? 

Challenge link: [here](https://felicity.iiit.ac.in/contest/extra/fastandfurious/)

## Write-up

The website outputs mathematical equations together with a field to sumbit the solution.

	Level 1
	
	Solve: (92 + 30)
	
	Answer:_________
	[Submit]

If the solution is correct and was provided fast enough, the game continues with the next level.
Whenever the answer was wrong, or the arrived too late the game restarts with level 1.

The provided python script uses the request module to solve this challenge, the equations are
solved with `eval`.
After 200 levels the flag is retrieved:

Flag: the_flag_is_6ffb242e3f65a2b51c36745b1cd591d1

## Other write-ups and resources

* https://www.youtube.com/watch?v=pmIVF0sxTUI
* https://github.com/pogTeam/writeups/tree/master/2017/BreakIn/Fast%20and%20Furious
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/fast_and_furious

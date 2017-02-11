# Break In 2017 - Fast and Furious


**Category:** Web
**Points:** 100
**Solves:** (TODO)
**Description:**

> Animesh and Aalekh are very good friends. Animesh always like things working at __Ultra fast speed__ and gave Aalekh a challenging task.
> He asks Aalekh to complete the task, after the completion of which, Animesh will give Aalekh a Juice Treat.
> Can you help Aalekh getting a Juice Treat? 

> Challenge link: [here](https://felicity.iiit.ac.in/contest/extra/fastandfurious/)

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

When you open the given link, you find 3 things.

1. Level index
2. Solve: <some random mathematical expression>
3. Answer text box with a submit button

When you normally try to submit the answer to the corresponding mathematical expression, the level index does not increase. Getting a hint from the problem statement "Fast and Furious", if you try to submit the answer really quick (within 3 seconds), you can see an increase in the level index. Thus the task was to automate the process of submitting the correct answer "really quick". An example javascript program for that is:

```javascript
var ans = eval(document.getElementsByTagName('p')[1].innerHTML.split(':')[1]);
var inputs = document.getElementsByTagName('input');
inputs[0].value = ans;
inputs[1].click();
```

On clearing 200 levels, you get the response as: `the_flag_is_6ffb242e3f65a2b51c36745b1cd591d1`

(See program `script.py` for complete solution)

Clearly the flag is `6ffb242e3f65a2b51c36745b1cd591d1`


__Extras__: Some people were having the curiosity that how are we maintaining the progress of a particular user even when we didn't have any login/other cookies to store that info. We actually did that on front end using the encrypted value of user level progress (in cookies), that we were verifying on the backend after decryption and modified accordingly :smile:

## Other write-ups and resources
* https://www.youtube.com/watch?v=pmIVF0sxTUI
* https://github.com/pogTeam/writeups/tree/master/2017/BreakIn/Fast%20and%20Furious
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/fast_and_furious

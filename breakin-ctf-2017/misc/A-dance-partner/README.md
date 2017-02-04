# Break In 2017 - A dance partner


**Category:** Misc
**Points:** 100
**Solves:** (TODO)
**Description:**

> Animesh and Ayushi are good friends. Ayushi is good at dancing but Animesh is not. 
> As Felicity is coming, Animesh, keeping his hacking skills aside, is trying to learn a Bollywood dance from Ayushi. As Ayushi knows that Animesh is not good at dancing, she teaches him only easy moves, such as moving forward, backward, right and left.
> Animesh, after lot of practise is now able dance well with those limited moves, but unfortunately he is unable to get any partner.
> Animesh asks his friend Aalekh for help, but instead of helping, Aalekh, based on Animesh's dance performance gave him a Jumbo Maze Puzzle hidden with a flag (sign of true friendship :P).
> Aalekh promises him that if he can extract the flag out of the Maze, he will get a partner for Animesh. As you all would have known Animesh very well till now, he want a dance partner at any cost, hence he asks you for the help to find the flag.

> Can you help Animesh find his dance partner? 

> Link to Jumbo maze [here](https://goo.gl/xGVsKk)

> (If the length of answer string exceeds 255, you need to submit the md5sum of the flag)

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

When you observe the RGB values or each block in the Jumbo Maze, you find that all the blocks (except the green starting block) have the RGB values of the type (x, x, x). If you observe closely, all such 'x' in the maze are corresponding to the ascii values of `0-9` and `a-z`.

The actual values associated with the blocks can be found [here](https://cloud.githubusercontent.com/assets/9266422/22561336/cbc2125e-e99d-11e6-8e8b-dcaf9fa16d48.jpg)

Hence you can obtain a 2d Array based on the ascii values of the maze.

Also when you observe the metadata associated with the image, you will find a comment as follows:
```
^[[A^[[D^[[C^[[A^[[C^[[C^[[B^[[D^[[A^[[A^[[A^[[A^[[D^[[D^[[D^[[C^[[B^[[A^[[B^[[B^[[A^[[C^[[C^[[D^[[C^[[B^[[C^[[D^[[A^[[B^[[A^[[D^[[B^[[C^[[C^[[A^[[B^[[C^[[A^[[D^[[B^[[C^[[C^[[C^[[D^[[D^[[C^[[C^[[B^[[A^[[A^[[C^[[C^[[C^[[D^[[B^[[B^[[C^[[A^[[B^[[A^[[C^[[C^[[C^[[A^[[D^[[D^[[D^[[B^[[A^[[A^[[A^[[D^[[C^[[C^[[C^[[C^[[D^[[A^[[D^[[A^[[D^[[D^[[B^[[C^[[C^[[D^[[B^[[B^[[A^[[A^[[B^[[A^[[A^[[C^[[B^[[A^[[D^[[A^[[D^[[B^[[D^[[D^[[C^[[D^[[D^[[B^[[A^[[D^[[D^[[C^[[A^[[D^[[A^[[C^[[A^[[A^[[B^[[B^[[C^[[A^[[B^[[A^[[D^[[A^[[B^[[C^[[A^[[B^[[D^[[D^[[B^[[C^[[D^[[B^[[A^[[C^[[B^[[B^[[B^[[B^[[D^[[C^[[C^[[C^[[C^[[D^[[B^[[C^[[B^[[B^[[D^[[B^[[A^[[D^[[C^[[A^[[B^[[D^[[D^[[A^[[B^[[D^[[C^[[B^[[B^[[A^[[D^[[A^[[D^[[B^[[C^[[B^[[A^[[D^[[D^[[D^[[B^[[D^[[B^[[C^[[D^[[C^[[D^[[B^[[A^[[A^[[A^[[D^[[C^[[A^[[A^[[C^[[B^[[C^[[C^[[B^[[C^[[C^[[B^[[B^[[A^[[D^[[B^[[C^[[B^[[D^[[D^[[A^[[C^[[D^[[B^[[B^[[B^[[B^[[D^[[D^[[B^[[C^[[B^[[C^[[C^[[B^[[C^[[C^[[C^[[A^[[C^[[C^[[A^[[C^[[C^[[B^[[D^[[C^[[D^[[D^[[D^[[D^[[D^[[B^[[D^[[C^[[C^[[B^[[C^[[D^[[B^[[D^[[C^[[C^[[C^[[C^[[B^[[D^[[C^[[D^[[B^[[D^[[A^[[C^[[C^[[B^[[C^[[D^[[C^[[A^[[A^[[B^[[D^[[B^[[C^[[D^[[A^[[D^[[B^[[D^[[A^[[B^[[C^[[D^[[B^[[C^[[B^[[A^[[B^[[A^[[B^[[B^[[C^[[B^[[D^[[C^[[A^[[C^[[B^[[C^[[B^[[D^[[D^[[B^[[C^[[D^[[D^[[A^[[B^[[A^[[D^[[D^[[D^[[D^[[C^[[A^[[A^[[B^[[B^[[D^[[A^[[C^[[A^[[A^[[B^[[B^[[C^[[A^[[D^[[A^[[B^[[C^[[D^[[D^[[A^[[D^[[D^[[C^[[A^[[A^[[D^[[C^[[C^[[A^[[C^[[C^[[B^[[D^[[A^[[A^[[C^[[B^[[B^[[C^[[A^[[A^[[C^[[A^[[B^[[C^[[B^[[C^[[C^[[A^[[C^[[C^[[C^[[B^[[C^[[C^[[C^[[C^[[B^[[C^[[A^[[D^[[C^[[A^[[A^[[B^[[C^[[D^[[C^[[C^[[C^[[D^[[A^[[B^[[D^[[B^[[C^[[C^[[B^[[B^[[A^[[D^[[A^[[D^[[B^[[A^[[C^[[A^[[A^[[A^[[A^[[B^[[C^[[A^[[C^[[C^[[D^[[B^[[D^[[D^[[C^[[C^[[B^[[C^[[B^[[C^[[B^[[C^[[B^[[B^[[D^[[A^[[B^[[A^[[C^[[A^[[D^[[D^[[B^[[C^[[C^[[C^[[D^[[B^[[A^[[B^[[A^[[A^[[C^[[A^[[D^[[B^[[A^[[C^[[A^[[D^[[A^[[D^[[D^[[D^[[C^[[D^[[A^[[A^[[C^[[B^[[B^[[D^[[C^[[C^[[A^[[B^[[B^[[C^[[D^[[C^[[B^[[D^[[B^[[D^[[C^[[C^[[D^[[D^[[B^[[D^[[B^[[C^[[A^[[A^[[C^[[B^[[B^[[A^[[A^[[A^[[B^[[C^[[D^[[A^[[C^[[A^[[C^[[D^[[D^[[C^[[D^[[A^[[D^[[D^[[D^[[A^[[C^[[D^[[D^[[A^[[B^[[D^[[D^[[B^[[A^[[B^[[C^[[D^[[C^[[C^[[A^[[B^[[C^[[B^[[B^[[B^[[B^[[C^[[A^[[D^[[A^[[D^[[B^[[B^[[D^[[D^[[D^[[B^[[D^[[A^[[C^[[D^[[C^[[C^[[D^[[C^[[A^[[C^[[B^[[D^[[B^[[B^[[C^[[A^[[B^[[A^[[C^[[D^[[D^[[D^[[C^[[C^[[D^[[D^[[A^[[B^[[D^[[D^[[D^[[C^[[C^[[B^[[D^[[D^[[B^[[B^[[A^[[B^[[B^[[C^[[A^[[A^[[A^[[C^[[D^[[D^[[A^[[D^[[A^[[B^[[C^[[C^[[C^[[B^[[D^[[D^[[D^[[D^[[C^[[D^[[D^[[B^[[C^[[D^[[B^[[B^[[C^[[D^[[B^[[C^[[C^[[D^[[B^[[D^[[C^[[A^[[C^[[C^[[D^[[B^[[D^[[B^[[D^[[A^[[B^[[B^[[B^[[A^[[D^[[C^[[C^[[C^[[C^[[C^[[A^[[D^[[B^[[C^[[A^[[B^[[D^[[B^[[D^[[B^[[B^[[B^[[D^[[C^[[B^[[B^[[B^[[C^[[B^[[A^[[D^[[C^[[C^[[A^[[D^[[A^[[B^[[A^[[D^[[D^[[B^[[A^[[D^[[B^[[C^[[B^[[A^[[D^[[B^[[C^[[D^[[C^[[A^[[B^[[D^[[D^[[D^[[C^[[B^[[B^[[A^[[D^[[D^[[B^[[D^[[D^[[C^[[C^[[D^[[D^[[A^[[B^[[C^[[D^[[D^[[C^[[C^[[D^[[A^[[C^[[A^[[C^[[A^[[D^[[B^[[C^[[A^[[C^[[B^[[C^[[B^[[A^[[D^[[B^[[D^[[A^[[D^[[C^[[A^[[B^[[B^[[D^[[C^[[A^[[C^[[A^[[D^[[D^[[B^[[C^[[D^[[C^[[B^[[C^[[C^[[C^[[B^[[A^[[D^[[B^[[A^[[A^[[D^[[A^[[D^[[D^[[C^[[B^[[D^[[D^[[C^[[D^[[B^[[B^[[A^[[A^[[C^[[A^[[A^[[A^[[A^[[D^[[C^[[D^[[A^[[B^[[C^[[A^[[A^[[C^[[D^[[C^[[D^[[C^[[D^[[A^[[C^[[B^[[C^[[D^[[C^[[B^[[A^[[D^[[B^[[B^[[B^[[B^[[B^[[C^[[A^[[A^[[A^[[A^[[D^[[C^[[C^[[A^[[C^[[B^[[D^[[C^[[D^[[A^[[A^[[B^[[D^[[C^[[A^[[A^[[C^[[B^[[D^[[B^[[C^[[D^[[D^[[C^[[B^[[C^[[A^[[D^[[A^[[D^[[A^[[B^[[D^[[D^[[B^[[A^[[D^[[D^[[A^[[D^[[D^[[D^[[A^[[C^[[A^[[B^[[D^[[D^[[B^[[B^[[B^[[D^[[D^[[A^[[A^[[C^[[B^[[B^[[B^[[C^[[C^[[A^[[C^[[B^[[B^[[D^[[B^[[B^[[C^[[B^[[D^[[D^[[A^[[A^[[B^[[D^[[C^[[C^[[C^[[C^[[B^[[A^[[C^[[C^[[C^[[D^[[D^[[D^[[B^[[C^[[D^[[B^[[D^[[D^[[B^[[B^[[D^[[C^[[C^[[D^[[D^[[A^[[A^[[D^[[C^[[C^[[C^[[B^[[C^[[A^[[D^[[D^[[C^[[A^[[A^[[D^[[C^[[C^[[D^[[D^[[A^[[B^[[B^[[D^[[D^[[A^[[B^[[B^[[D^[[C^[[B^[[D^[[A^[[B^[[C^[[C^[[B^[[D^[[C^[[C^[[C^[[C^[[C^[[C^[[D^[[A^[[B^[[D^[[A^[[A^[[B^[[D^[[C^[[B^[[D^[[D^[[A^[[C^[[C^[[B^[[A^[[A^[[C^[[C^[[B^[[D^[[A^[[A^[[B^[[A^[[A^[[D^[[C^[[C^[[C^[[B^[[A^[[B^[[D^[[D^[[C^[[D^[[B^[[A^[[B^[[B^[[A^[[A^[[A^[[B^[[D^[[D^[[D^[[B^[[C^[[D^[[C^[[A^[[D^[[B^[[A^[[A^[[D^[[A^[[D
```

Now the hint for the above content was given in the question. Animesh learns only the easy steps, which were "forward, backward, right and left". Also the above code is nothing but the values obtained by pressing up, down, right left keys (where ^[[A: Up, ^[[B: Down, ^[[C: Right, ^[[D: Left). Hence when you follow the same path in the given image (starting with the Green block) you obtain the path as follows:
```
x8xxbzu1btgh6zvz9z9e9ygygtitgtgyotipi3jpi3oio3oihiotdndtrj5j5toos8nn5nrxtxx4f4o7pmkbp7pxrxpxpmp7pmy4kmqmqyjybobwj70c2c04j4jc2cj4jce707j70wb3gxgnmmmc8t1ihioioio3j3i3909zitbzuzbx18x8j8j8a8xwzwv29eotbz90g0uxgwprnxnr10zhcn5rtimdbfpdvyb48k8kvdpzbdbfk9k6w6z6hmcmccj9cmxfxfa7amxfxmccj9jcjf3q3q3qbe3l3e93z5mkece3t3tfx373n9n37kn939nx0939093tuuuq000xpsfwlsw6fwj9z6a6hmae66azveelkipvkvhrhdhdi1inid9ezn1npe919einakakjccc8kak8kxx1zq10hihi1qzjbi1h10101qp4cqc4bazp1818c2pc181pqptatac1zjzqzjb4x6bjzihiz1zqz1cabatatp18kjcjkqkcgxgx1x1akakw1zn49z1iep1piladidipipv91px56r6r8rxlxrxlila898am4uxdxd22vl4m4u9tyt98am4u5y5yhumuscrccc6c3v3c6u6a3bmvmodowotym2ijm2i2m0fv43w3hval3lalrvvzvzhm2m012s21qsqs2sqfnf909c0w4e4w4efe4e9e4efyun65un6mnf9fnc0nun6n0y0nnm65unun0c99k9909fnm656nu7u7fef7u5bu2f2f2f29hwhwhwhxzwuwu2uwl42u6mb8u2l2pldlplplwlulwjmowldlulpldlwqrqzxhxq3o5kwcvdvcuas9vd70zfv3cxqrmb9q4smlkw9wxw4sx2x8obo8x2s2gyeycqcicq8tatey6tgyeyms4sxs4q4lkixia1aud1du8qnqcib9e9c9btgt6tbicy6tbtgw7fcwsws8x8ob5b5asaswswcws8s2mleyeymlel4w9z
```
The md5sum of the above path is: `f524415e198cbc8983ac0bed3d0cbcef` which is the required flag.

## Other write-ups and resources
* https://github.com/USCGA/writeups/tree/master/online_ctfs/breakin_2017/a_dance_partner

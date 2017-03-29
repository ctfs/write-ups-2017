# AlexCTF: RE4: unVM me

**Category:** Reverse Engineering
**Points:** 250
**Solves:** 334
**Description:**

> If I tell you what version of python I used .. where is the fun in that?

## Write-up

We're given a `.pyc` file, so we use `uncompyle` to try to turn it back to Python source (note this is python2.7 source):
`uncompyle2 -o unvme.py unvm_me.pyc`

The resulting `unvm.py`:

	#Embedded file name: unvm_me.py
	import md5
	md5s = [174282896860968005525213562254350376167L,
	 137092044126081477479435678296496849608L,
	 126300127609096051658061491018211963916L,
	 314989972419727999226545215739316729360L,
	 256525866025901597224592941642385934114L,
	 115141138810151571209618282728408211053L,
	 8705973470942652577929336993839061582L,
	 256697681645515528548061291580728800189L,
	 39818552652170274340851144295913091599L,
	 65313561977812018046200997898904313350L,
	 230909080238053318105407334248228870753L,
	 196125799557195268866757688147870815374L,
	 74874145132345503095307276614727915885L]
	print 'Can you turn me back to python ? ...'
	flag = raw_input('well as you wish.. what is the flag: ')
	if len(flag) > 69:
		print 'nice try'
		exit()
	if len(flag) % 5 != 0:
		print 'nice try'
		exit()
	for i in range(0, len(flag), 5):
		s = flag[i:i + 5]
		if int('0x' + md5.new(s).hexdigest(), 16) != md5s[i / 5]:
			print 'nice try'
			exit()

	print 'Congratz now you have the flag'

With a bit of inspection, we see that if the flag is the right size - less than 70 characters, and divisible by 5 - the for loop takes the `md5` hash of each 5-digit slice of the input and compares them against each value in the list `md5s`. We can use online lookup tables to lookup the hashes, but first we have to convert them each to hex:

	>>> for m in md5s:
	>>>		print "{:02X}".format(m)
	831DAA3C843BA8B087C895F0ED305CE7
	6722F7A07246C6AF20662B855846C2C8
	5F04850FEC81A27AB5FC98BEFA4EB40C
	ECF8DCAC7503E63A6A3667C5FB94F610
	C0FD15AE2C3931BC1E140523AE934722
	569F606FD6DA5D612F10CFB95C0BDE6D
	68CB5A1CF54C078BF0E7E89584C1A4E
	C11E2CD82D1F9FBD7E4D6EE9581FF3BD
	1DF4C637D625313720F45706A48FF20F
	3122EF3A001AAECDB8DD9D843C029E06
	ADB778A0F729293E7E0B19B96A4C5A61
	938C747C6A051B3E163EB802A325148E
	38543C5E820DD9403B57BEFF6020596D

Note that the 7th hash is one character too short: this is because python got rid of a leading zero. After finding these hex hashes, we just use a lookup table like https://hashkiller.co.uk/md5-decrypter.aspx, and we get the results:  

	831daa3c843ba8b087c895f0ed305ce7 MD5 : ALEXC
	6722f7a07246c6af20662b855846c2c8 MD5 : TF{dv
	5f04850fec81a27ab5fc98befa4eb40c MD5 : 5d4s2
	ecf8dcac7503e63a6a3667c5fb94f610 MD5 : vj8nk
	c0fd15ae2c3931bc1e140523ae934722 MD5 : 43s8d
	569f606fd6da5d612f10cfb95c0bde6d MD5 : 8l6m1
	068cb5a1cf54c078bf0e7e89584c1a4e MD5 : n5l67
	c11e2cd82d1f9fbd7e4d6ee9581ff3bd MD5 : ds9v4
	1df4c637d625313720f45706a48ff20f MD5 : 1n52n
	3122ef3a001aaecdb8dd9d843c029e06 MD5 : v37j4
	adb778a0f729293e7e0b19b96a4c5a61 MD5 : 81h3d
	938c747c6a051b3e163eb802a325148e MD5 : 28n4b
	38543c5e820dd9403b57beff6020596d MD5 : 6v3k}

So the flag is:
`ALEXCTF{dv5d4s2vj8nk43s8d8l6m1n5l67ds9v41n52nv37j481h3d28n4b6v3k}`

## Other write-ups and resources

 * http://r.rogdham.net/28
 * http://ronins.team/alexctf_re4_unvm_me/
 * https://team-nawhack.fr/2017/02/07/alexctf-2017-re4/
 * https://0xd13a.github.io/ctfs/alexctf2017/unvm-me
 * http://fadec0d3.blogspot.com/2017/02/alexctf-2017-reverse-engineering-gifted.html
 * http://mistake.com/
 * http://writeups.ctflearn.com/alexctf-writeups-2/
 * https://www.youtube.com/watch?v=qeGaVVpjOL4
 * https://github.com/KevOrr/ctf-writeups/tree/master/alexctf-2017/reversing/250-unVM_me
 * https://advancedpersistentjest.com/2017/02/06/writeups-catalyst-unvm-me-unknown-format-mailclient/
 * http://70ry.tistory.com/entry/AlexCTF-Reverse-Engineering
 * https://github.com/pogTeam/writeups/tree/master/2017/AlexCTF/re4
 * http://duksctf.github.io/AlexCTF2017-unVMme/
 * https://drive.google.com/open?id=0B6pr1LpSJl7iQTVXOHlCMnFnMFE
 * https://github.com/ChalmersCTF/Writeups/tree/master/AlexCTF%202017-02-05/re4
 * https://ngaoopmeo.blogspot.com/2017/02/alexctf-2017writeupre4-unvm-me.html
 * http://drizbit.com/post/alexctf-reverse-engineering-2017/
 * http://g4ngli0s.logdown.com/posts/1390245-alexctf2017-re4-unvm-me
 * http://countersite.org/articles/reverse_engineering/136-revers-s-alexctf-2017.html

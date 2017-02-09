# Break In 2017 - Mysterious GIF



**Category:** Misc
**Points:** 100
**Solves:** (TODO)
**Description:**

> Aalekh is a die hard fan of Felicity and he decided to make a GIF (Graphics Interchange Format) based on this year's Felicity theme.
> One fine day, Parth, an Anime lover gives Aalekh and Animesh a flag to hide it in a GIF. Suddenly Aalekh remembers of his GIF he generated before and decided to hide the flag in it.
> He believes that the flag is so mysterious that only those who are a fan of Felicity can find the flag. Are you a fan of felicity? If yes, then find the flag 

> Download the Mysterious GIF from [here](https://goo.gl/YQq3js)

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

The given GIF when analyzed with `binwalk` gives you the following information
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             GIF image data, version "89a", 440 x 608
2670386       0x28BF32        Zip archive data, at least v1.0 to extract, compressed size: 112890, uncompressed size: 112890, name: temp.zip
2783320       0x2A7858        End of Zip archive
2783420       0x2A78BC        End of Zip archive
```

As we can see, it's much more than just a GIF, some extra zip file is also present at the last of the GIF.

The original size of the given GIF is: 2783442 bytes. Hence when you extract the last 2783442-2670386, i.e. 113056 bytes, you get a zip file, which on extracting gives a zip file again by the name of `temp.zip`. This file is not actually a zip file (which can be found by using binwalk again on temp.zip), but rather it's a concatenation of several (265) encrypted files, starting from partaa.enc and going till partke.enc

Now the next target is to find a way to decrypt these encrypted files.

On observing the metadata associated with each frames of the given GIF, you can observe the following lines in each frame.
```
comment: 4d494945767749424144414e42676b71686b6947397730424151454641415343424b6b776767536c41674541416f4942415144644d4e624c3571565769435172
comment: 5832773639712f377933536849507565707478664177525162524f72653330633655772f6f4b3877655a547834346d30414c6f75685634364b63514a6b687271
comment: 67384f79337335593546563177434b3736367532574c775672574d49554a47316a4444725276595049635135557143703545445143696f524d4763555a456732
comment: 75766c3134324c44424161654f4c7a464d3465324a637a532b307238356d5052724353786a4c4b4c614c774949516e5a58497058535552562f776a6877575231
comment: 664a474738512b7563454170615873634e435546343462506d344850434a2f306d7244435457482f59324350564a6b4e6b2b6f305637564f74484b734d4c344e
comment: 434e414a483434572f4952774a6e744e572b4e3848726770526b467567686d4e6a63776c456b7274554b4731735243792f2f57687544756e5632706853525176
comment: 486f74425a76796441674d424141454367674542414a79614e336d6c6b756e772b617137704b5561677636437a6442477964394a78447941706b314b374f4938
comment: 54426873464d2f33744246654131592f41762b7568434c727967726b4279652f6963372f2b30356f3853392b65674d6b52584e484b41757952336752696b7759
comment: 7678454b634a676a5a5a4c524656794159372f6c477634774e42683362495044664631446739737a596e6b774948396c4c454679656d4d3734416941596c6371
comment: 6456645a49452f6271325a344a4f307439484367485a4e6651374a645266656a4e4a51565955443031517535644d744f523465494d6462576b68625658773254
comment: 45304837785178746a7754367a557270714576764f376533464845734249583635565258524c6276394f6f61794a786352715838654a6b5269344c2f597a6f34
comment: 4b5470456d6b64754a4c58734677743361715154626a5a48584f6c5454344e45647348327030547343414543675945412f653162737a4f3061312b6342614451
comment: 6a514f2b50763942734a464442336f314c477555484d4e53384644706e334a3436556b59796b353276496130763454636a715353484e4976585730544445556b
comment: 624e4641314870557856786c7730426965656838426733486658795142685876645444376b306c73446d4d456f3455504b59533644356359577972776864356e
comment: 4344304c72786562674f373552784c35514549452b34435649516b4367594541337638522f584b52564a50453461456567377051347554766346786a454e4e65
comment: 787866364b34787059344c6639636c49766465635268433274314864522b7853756c552f52536152727a4863773378672b4c31754f3073317435533766336e75
comment: 3361696849586b636747537158435a3156487a426d65433430545673664179627337714a30785936543571384d6e78324f62355a336c49477579686a65566174
comment: 4649493253647a324a2f55436759454174654131357a516f6a53504e482b62676d62424e717465763247556a536f374932556b777243316e4559515334636266
comment: 5064444364643066684d6444585534766e2b66575539686b58706d4b7043592b416363626c56554e744e4d4b6649423453484d78716a426961386f31616e5a35
comment: 726b6e6f5638576d4a4f50645a6259666478422f4b4432454434444243464756494c79417975657731506657436f64586969502f5a356a67742b6b4367594541
comment: 727378716f61306f316f3975695237752b48735835494e6f5854394f4f475933715144576a55526e61435779774d756a525979355a774b363930416f6f4c5253
comment: 744e555633334b3453416868384b7153714f6830652b34636b5762354170666c38634b3561362b76383854303958384141645935504247335465622b7673357a
comment: 54704d75626c54434b4a773259617a4754385579564e38666635334e4f3951426f4533686d45796f642f4543675941396b307879434a7a6376654b6478727936
comment: 706a51786b39465a7a3341744570316f635635566f776167562b4f4e657a2f4863634638474a4f384244716c5036586b634c5574736e70367459526545494349
comment: 484b7735432b667741586c4649746d30396145565458772b787a4c4a623253723667415450574d35715661756278667362356d58482f77443969434c684a536f
comment: 724b3052485a6b745062457335797444737142486435504646773d3d
```

Which is clearly some hexadecimal strings, decoding which gives you the following result:
```
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDdMNbL5qVWiCQr
X2w69q/7y3ShIPueptxfAwRQbROre30c6Uw/oK8weZTx44m0ALouhV46KcQJkhrq
g8Oy3s5Y5FV1wCK766u2WLwVrWMIUJG1jDDrRvYPIcQ5UqCp5EDQCioRMGcUZEg2
uvl142LDBAaeOLzFM4e2JczS+0r85mPRrCSxjLKLaLwIIQnZXIpXSURV/wjhwWR1
fJGG8Q+ucEApaXscNCUF44bPm4HPCJ/0mrDCTWH/Y2CPVJkNk+o0V7VOtHKsML4N
CNAJH44W/IRwJntNW+N8HrgpRkFughmNjcwlEkrtUKG1sRCy//WhuDunV2phSRQv
HotBZvydAgMBAAECggEBAJyaN3mlkunw+aq7pKUagv6CzdBGyd9JxDyApk1K7OI8
TBhsFM/3tBFeA1Y/Av+uhCLrygrkBye/ic7/+05o8S9+egMkRXNHKAuyR3gRikwY
vxEKcJgjZZLRFVyAY7/lGv4wNBh3bIPDfF1Dg9szYnkwIH9lLEFyemM74AiAYlcq
dVdZIE/bq2Z4JO0t9HCgHZNfQ7JdRfejNJQVYUD01Qu5dMtOR4eIMdbWkhbVXw2T
E0H7xQxtjwT6zUrpqEvvO7e3FHEsBIX65VRXRLbv9OoayJxcRqX8eJkRi4L/Yzo4
KTpEmkduJLXsFwt3aqQTbjZHXOlTT4NEdsH2p0TsCAECgYEA/e1bszO0a1+cBaDQ
jQO+Pv9BsJFDB3o1LGuUHMNS8FDpn3J46UkYyk52vIa0v4TcjqSSHNIvXW0TDEUk
bNFA1HpUxVxlw0Bieeh8Bg3HfXyQBhXvdTD7k0lsDmMEo4UPKYS6D5cYWyrwhd5n
CD0LrxebgO75RxL5QEIE+4CVIQkCgYEA3v8R/XKRVJPE4aEeg7pQ4uTvcFxjENNe
xxf6K4xpY4Lf9clIvdecRhC2t1HdR+xSulU/RSaRrzHcw3xg+L1uO0s1t5S7f3nu
3aihIXkcgGSqXCZ1VHzBmeC40TVsfAybs7qJ0xY6T5q8Mnx2Ob5Z3lIGuyhjeVat
FII2Sdz2J/UCgYEAteA15zQojSPNH+bgmbBNqtev2GUjSo7I2UkwrC1nEYQS4cbf
PdDCdd0fhMdDXU4vn+fWU9hkXpmKpCY+AccblVUNtNMKfIB4SHMxqjBia8o1anZ5
rknoV8WmJOPdZbYfdxB/KD2ED4DBCFGVILyAyuew1PfWCodXiiP/Z5jgt+kCgYEA
rsxqoa0o1o9uiR7u+HsX5INoXT9OOGY3qQDWjURnaCWywMujRYy5ZwK690AooLRS
tNUV33K4SAhh8KqSqOh0e+4ckWb5Apfl8cK5a6+v88T09X8AAdY5PBG3Teb+vs5z
TpMublTCKJw2YazGT8UyVN8ff53NO9QBoE3hmEyod/ECgYA9k0xyCJzcveKdxry6
pjQxk9FZz3AtEp1ocV5VowagV+ONez/HccF8GJO8BDqlP6XkcLUtsnp6tYReEICI
HKw5C+fwAXlFItm09aEVTXw+xzLJb2Sr6gATPWM5qVaubxfsb5mXH/wD9iCLhJSo
rK0RHZktPbEs5ytDsqBHd5PFFw==
```

Which is nothing but a private key (which will later be used to decrypt those .enc files).
Again when you look at the actual size of the .enc files, you find them to be exactly 256 bytes, which is the size of the encrypted file created when you use a rsa public key to encrypt a file. Hence we can guess from here that the given .enc files are the ones which were encrypted with a public key, whose corresponding private key is obtained from the metadata.

Use this private key to decrypt all those partaa.enc ... partke.enc and let's save the decrypted files by the name (say) partaa, partab, ... partke
(This can be done using `openssl rsautl -decrypt -inkey private_key_breakin -in encrypted_file -out decrypted_file`)

Clearly these are the parts which are obtained when we use `split` command on a particular file. Hence we just simply concatinate them using `cat part* > final`
On observing the file `final`, we see that the given file is an image. Open the image (link [here](https://goo.gl/LeNzrw)) and you get your flag. 

The flag is `FelicityIsFun`

## Other write-ups and resources
* none yet
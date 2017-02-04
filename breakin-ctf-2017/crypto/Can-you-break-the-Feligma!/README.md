# Break In 2017 - Can you break the Feligma!


**Category:** Crypto
**Points:** 100
**Solves:** 0
**Description:**

> Aalekh, after getting tired of using all the widely known encryption algorithm designed his own algorithm, known as "Feligma", to encrypt a secret message (really secret).
> Now he wants to check how strong his encryption is and asks you to break the encryption. The target is to break the algorithm and find the secret key encoded by Aalekh. 

> The only hint he gave you is the key he used to encrypt his secret message, which is: 100003

## Write-up

by [ironmaniiith](https://github.com/ironmaniiith)

The two important hints that were given during the contest were:

1. The key used for encryption may not work during decryption
2. RESET_VAL and STEP need not be changed

It was given that the encrypted code obtained after encrypting the secret message with Feligma Encryption algorithm was: `)fk~y+ &y{(@ &tqn!-`

There are some points to note before actually trying to break the Feligma Encryption. These are

* All the addition, subtraction and multiplication is performed over modulo 41 (TOTAL_CHARS) number space.
* The `transform` function used in the encryption ONLY depends on the given number and the index of `CONFIG` at which it is applied
```javascript
function transform(n, idx) {
    return (n * modExpo(KEY, idx, TOTAL_CHARS)) % TOTAL_CHARS;
}
```
* The `encrypt` function performs encryption in two major operations, which are `forwardPass` and `backwardPass` and updates the `CONFIG` every time it is called.
```javascript
function encrypt(n) {
    var aux = forwardPass(n);
    var encrypted_code = backwardPass(aux);
    updateConfig();
    return encrypted_code;
}
``` 
The main thing that was unknown was the `CONFIG` that was used to encrypt the original message. Also the key that was used during the encryption was given (100003). Now when you try to play with feligma using any random secret messages with a particular `CONFIG`, you may find that the same message DO NOT decrypt to the original secret message with the original KEY that is used to encrypt the message.

* The CONFIG gets updated by value 1 each time the encrypt function is called, this happens in a circular manner, i.e. whenever the value at a particular index of CONFIG reaches the `TOTAL_CHARS`, which is in this case 41, it resets it's original value and increase the next index value of CONFIG. This is exactly same as the milometer of a vehicle (or if you are familiar with Enigma machine, this concept is similar to wheels used Enigma machine)

i.e. 
After each iteration, whenever `updateConfig` function is called, `CONFIG` changes as follows (starting from say `[10, 30, 23, 37]`:
  1. `[10, 30, 23, 37]`
  2. `[10, 30, 23, 38]`
  3. `[10, 30, 23, 39]`
  4. `[10, 30, 23, 40]`
  5. `[10, 30, 24, 0]`
  6. `[10, 30, 24, 1]`
  7. `[10, 30, 24, 2]`
  8. `[10, 30, 24, 3]`

and so on...

* `forwardPass` and `backwardPass` function performs the complimentary operations (forwardPass is performing addition and backwardPass is performing subtraction over the given modulo space). Hence whatever output you get from the backwardPass, when fed to forwardPass will give you the original message (or code) used for encryption (However in order to make this thing happen, we need some extra efforts, we will see how exactly this will be done)

Now lets encrypt the `SECRET_WORD="hello world"` and let the CONFIG be `[24, 32, 10, 34, 30]`
The encrypted output is obtained using: `getEncryptedCode(SECRET_WORD)`, which gives the encrypted message as: `e-y+f !-w)n`

Next set the value of `SECRET_WORD` as the obtained encrypted message (i.e. `SECRET_WORD="e-y+f !-w)n"`), and try to decrypt it in the same manner by calling `getEncryptedCode` function. Unfortunately we are not able to decrypt it and we get the output as: `-$z{o c*sah`, which is NOT our original message.

However just try the same approach with the value of KEY as 31 (Just try, don't ask why for now :P )

Tada!!

We get the original message "hello world" back when we used the `KEY` as 31 and the same `CONFIG` that we used for encryption. Now let's try to understand why it is happening so.

The entities reponsible for mapping the numbers to their encrypted values are given by `num_maps` and `rev_num_maps`. There is one more entity known as `flip_map` which is nothing but a mapping of the form: f(x) = y <=> f(y) = x i.e. if x if given as input to flip_map, y is obtained and vice versa.

```javascript
var flip_map = {
    0: 38, 1: 26, 2: 35, 3: 15, 4: 14, 5: 6,
    6: 5, 7: 7, 8: 34, 9: 16, 10: 28,
    11: 19, 12: 17, 13: 22, 14: 4, 15: 3,
    16: 9, 17: 12, 18: 39, 19: 11, 20: 32,
    21: 25, 22: 13, 23: 30, 24: 31, 25: 21,
    26: 1, 27: 37, 28: 10, 29: 33, 30: 23,
    31: 24, 32: 20, 33: 29, 34: 8, 35: 2,
    36: 40, 37: 27, 38: 0, 39: 18, 40: 36
};
```

We also see an entity char_map appearing in feligma encryption, which is nothing but just a mapping of some special characters to the numbers.

Now we have following things to note here regarding these maps.

1. flip_map[x] = y <=> flip_map[y] = x
2. For any `num_map` given by num_maps[i], we have num_map[x] = y => rev_num_maps[y] = x and vice versa.
3. A total of 5 num_map are used (num_maps[i], 0 <= i <= 4) which are used at the corresponding indices of `CONFIG`. i.e. `CONFIG[idx]` uses the num_map (and rev_num_map) defined by `num_maps[idx]` and `rev_num_maps[idx]`

Next, regarding the `transform` function, we see that for all the values that lie in modulo 41 space, `transform` function is just a one-one mapping of these numbers (n) when used with a "Prime" `KEY`. (Can be proved easily!)

Now let's see how exactly the encryption, decryption and breaking of Feligma Encryption Algorithm works.

Here's what a single iteration of forwardPass looks like
![feligma_1](https://cloud.githubusercontent.com/assets/9266422/22618450/639695d6-eb02-11e6-85b7-f70bfb7e1a7e.jpg)

i.e. for a given index `idx`, the forwardPass proceeds as follows:

1. Takes an input 'n'
2. Add the value of CONFIG[idx] to 'n' (over given modulo space)
3. Transform the value obtained above (using `transform` function)
4. Feed the value obtained in step 3 to num_map and obtain an intermediate output.
5. The intermediate output is again transformed using the `transform` function and the final output is returned

Hence assuming that we have a 3 length `CONFIG` (the original problem had 5 length `CONFIG`), the complete forwardPass looks like:

![feligma_2](https://cloud.githubusercontent.com/assets/9266422/22619045/99cfe6c0-eb11-11e6-9e18-7bc906bd4702.jpg)

Towards the termination of forwardPass, the output from the last `CONFIG` is fed to flip_map.

The same logic goes with the backwardPass, the only difference being, instead of having an addition with CONFIG[idx], we have a subtraction with CONFIG[idx], over the given modulo space. Here lies the fact that when the final output returned from backwardPass is again fed to feligma (with some modifications with KEY), we are able to obtain the original codeword that was encrypted (You can understand forwardPass and backwardPass as mirror image of each other)

The backwardPass for 3 iterations looks like:
![feligma_3](https://cloud.githubusercontent.com/assets/9266422/22619046/99d11f72-eb11-11e6-94f6-d45bc5c3d20f.jpg)

Now let's see how we can decrypt (and eventually break the feligma)

The only problem that we will have during the decryption of feligma is that, we do not get back the original keyword that was encrypted using a particular `CONFIG` and `KEY`, even when we give the same `CONFIG` and `KEY`, the problem lies with `transform` function!!

Let's see what happens during the encryption of a particular code (we will call it 'n', i.e. the input fed to feligma as 'code' from now onwards) over a single length CONFIG (The same idea can be extended to multiple length `CONFIG` as well)

![feligma_4](https://cloud.githubusercontent.com/assets/9266422/22619047/99d4b556-eb11-11e6-926e-bfcaa6732bee.jpg)

Now we want to achieve that: The obtained n' from our code (n) when fed to feligma should return the original code.

For this to work, we need to have such a transform that will UNROLL the complete steps from 10 to 1 (as shown in the image above), when n' is fed as input to feligma

When you try to observe the role that `transform` function is playing, we can clearly see that it always comes as a multiplication term on whatever number it is applied to. Hence if we need to UNROLL the steps and obtain the original, we need to multiply such a term that will lead to a scenario where:
Initially obtained output: n * T (say n')
Output obtained during decryption: n' * T' or n * T * T'

If we want the output obtained during decryption to be as same as n, we can clearly say that
T * T' = 1 (over modulo 41)

Thus we can conclude that the transforms T and T' are "Multiplicative Inverse" of each other, and since these transforms only depend on the `KEY` used during the encryption (or decryption), we need to perform the decryption with a KEY', such that KEY' = MultipicativeInverse(KEY).

This was the reason why we were getting the same output "hello world" back with the KEY as 31 (because 31 is the multiplicate inverse of 100003 over modulo 41)

![feligma_5](https://cloud.githubusercontent.com/assets/9266422/22619048/99d7807e-eb11-11e6-8db2-acde1c54225b.jpg)

![feligma_6](https://cloud.githubusercontent.com/assets/9266422/22619049/99da5eb6-eb11-11e6-9de1-31e15316447e.jpg)

Hence we now know the `KEY` that will be used to decrypt the original encryption, but that's not all!!

We also need to know the `CONFIG` that was used originally to encrypt our secret message.
Now here comes the brute force part, now we will just brute force all the possible `CONFIG` in order to obtain the required `CONFIG`.

Even an "unoptimized" brute solution will work here and will give results in around 8-10 mins, which is as follows:
```javascript
SECRET_WORD = ")fk~y+ &y{(@ &tqn!-"
function brute() {
    for (var i = 0; i < TOTAL_CHARS; i++) {
        for (var j = 0; j < TOTAL_CHARS; j++) {
            for (var k = 0; k < TOTAL_CHARS; k++) {
                for (var l = 0; l < TOTAL_CHARS; l++) {
                    for (var m = 0; m < TOTAL_CHARS; m++) {
                        CONFIG = [i, j, k, l, m];
                        var decoded_word = getEncryptedCode(SECRET_WORD);
                        var isSecret = (md5(decoded_word) === 'a78275598ed616d21a524787a573f9b7');
                        if (isSecret) {
                            console.log('Secret found:', decoded_word);
                            console.log('Config used for encryption:', CONFIG);
                            return;
                        }
                    }
                }
            }
        }
    }
}
brute();
```

You can optimize your brute even more if you carefully watch the `transform` function. Since it is returning values based on only the indices of `CONFIG` (which in this case varies from 0 to 4) and the `KEY`, you can "pre-compute" those values and can just return those values (along with multiplication of given `n`)
```javascript
/** Precomputation */
var dp = [];
for (var i = 0; i < CONFIG.length; i++) {
    dp[i] = modExpo(KEY, i, TOTAL_CHARS);
}

/** The function transform changes as follows: */
function transform(n, idx) {
    return (n * dp[idx]) % TOTAL_CHARS;
}
```

Thus when you apply the brute with the KEY 31, you get the final `CONFIG` as: `[24, 40, 18, 23, 37]` and the obtained secret message is: "__elakha isekl inava!__"

Clearly the md5sum (a78275598ed616d21a524787a573f9b7), which was given as the original message signature, matches with the md5sum of obtained decrypted message :-)

Hence the flag is `elakha isekl inava!`

## Other write-ups and resources
* none yet
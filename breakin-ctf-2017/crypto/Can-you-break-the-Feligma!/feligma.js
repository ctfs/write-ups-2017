var ASCII_OFFSET = 'a'.charCodeAt(0);
var TOTAL_CHARS = 41;
var RESET_VAL = 0;
var STEP = 1;
var SECRET_WORD = 'e-y+f !-w)n';
var CONFIG = [24, 32, 10, 34, 30];
var KEY = 31;

var hasOwnProperty = Object.prototype.hasOwnProperty;

function modExpo(base, expo, mod) {
    var ans = 1;
    base = base % mod;
    while (expo > 0) {
        if (expo & 1) ans = (ans * base) % mod;
        base = (base * base) % mod;
        expo >>= 1;
    }
    return ans % mod;
}

function transform(n, idx) {
    return (n * modExpo(KEY, idx, TOTAL_CHARS)) % TOTAL_CHARS;
}

function getChar(n) {
    if (n >= 26) {
        return rev_char_map[n];
    }
    return String.fromCharCode(n + ASCII_OFFSET);
}

function getCharCode(c) {
    if (hasOwnProperty.call(char_map, c)) {
        return char_map[c];
    }
    return c.charCodeAt(0) - ASCII_OFFSET
}

function updateConfig(idx) {
    idx = (idx === undefined) ? 0 : idx;
    if (idx >= CONFIG.length) return;
    if (CONFIG[idx] === TOTAL_CHARS - 1) {
        CONFIG[idx] = RESET_VAL;
        updateConfig(idx + 1);
    } else {
        CONFIG[idx] += STEP;
    }
}

function forwardPass(n, idx) {
    idx = (idx === undefined) ? 0 : idx;
    if (idx >= CONFIG.length) return flip_map[n];
    var input = transform((n + CONFIG[idx]) % TOTAL_CHARS, idx);
    var output = transform(num_maps[idx][input], idx);
    return forwardPass(output, idx + 1);
}

function backwardPass(n, idx) {
    idx = (idx === undefined) ? CONFIG.length - 1 : idx;
    var input = n;
    if (idx + 1 < CONFIG.length) input = (n - CONFIG[idx + 1] + TOTAL_CHARS) % TOTAL_CHARS;
    if (idx < 0) return input;
    input = transform(input, idx);
    var output = transform(rev_num_maps[idx][input], idx);
    return backwardPass(output, idx - 1);
}

function encrypt(n) {
    var aux = forwardPass(n);
    var encrypted_code = backwardPass(aux);
    updateConfig();
    return encrypted_code;
}

/** ############################################### */
/** Below are the various maps used for "Feligma Encryption Algorithm" */
var char_map = {
    '~': 26, '!': 27, '@': 28, '#': 29, '$': 30,
    '%': 31, '^': 32, '&': 33, '*': 34, '(': 35,
    ')': 36, '-': 37, '+': 38, '{': 39, '}': 40
};
var rev_char_map = {},
    num_maps = [],
    rev_num_maps = [];

num_maps[0] = {
    0 : 31, 1 : 36, 2 : 18, 3 : 6, 4 : 33, 5 : 25,
    6 : 28, 7 : 32, 8 : 24, 9 : 29, 10 : 21,
    11 : 35, 12 : 30, 13 : 23, 14 : 40, 15 : 38,
    16 : 20, 17 : 2, 18 : 0, 19 : 13, 20 : 27,
    21 : 9, 22 : 14, 23 : 39, 24 : 4, 25 : 12,
    26 : 7, 27 : 34, 28 : 37, 29 : 26, 30 : 22,
    31 : 3, 32 : 10, 33 : 1, 34 : 15, 35 : 8,
    36 : 5, 37 : 19, 38 : 17, 39 : 16, 40 : 11
};

num_maps[1] = {
    0 : 17, 1 : 39, 2 : 28, 3 : 16, 4 : 37, 5 : 7,
    6 : 10, 7 : 19, 8 : 20, 9 : 6, 10 : 15,
    11 : 1, 12 : 12, 13 : 36, 14 : 33, 15 : 18,
    16 : 38, 17 : 35, 18 : 4, 19 : 30, 20 : 9,
    21 : 24, 22 : 26, 23 : 34, 24 : 2, 25 : 8,
    26 : 14, 27 : 32, 28 : 27, 29 : 21, 30 : 3,
    31 : 22, 32 : 0, 33 : 25, 34 : 31, 35 : 23,
    36 : 11, 37 : 40, 38 : 13, 39 : 5, 40 : 29
};

num_maps[2] = {
    0 : 36, 1 : 11, 2 : 27, 3 : 24, 4 : 38, 5 : 22,
    6 : 13, 7 : 7, 8 : 5, 9 : 14, 10 : 9,
    11 : 20, 12 : 1, 13 : 29, 14 : 35, 15 : 10,
    16 : 2, 17 : 16, 18 : 28, 19 : 0, 20 : 25,
    21 : 26, 22 : 30, 23 : 21, 24 : 4, 25 : 37,
    26 : 33, 27 : 31, 28 : 12, 29 : 6, 30 : 3,
    31 : 8, 32 : 32, 33 : 40, 34 : 18, 35 : 23,
    36 : 15, 37 : 17, 38 : 34, 39 : 39, 40 : 19
};

num_maps[3] = {
    0 : 11, 1 : 38, 2 : 12, 3 : 33, 4 : 5, 5 : 14,
    6 : 29, 7 : 4, 8 : 21, 9 : 22, 10 : 19,
    11 : 35, 12 : 31, 13 : 20, 14 : 30, 15 : 16,
    16 : 24, 17 : 23, 18 : 39, 19 : 10, 20 : 1,
    21 : 0, 22 : 7, 23 : 27, 24 : 13, 25 : 37,
    26 : 2, 27 : 26, 28 : 25, 29 : 40, 30 : 34,
    31 : 6, 32 : 3, 33 : 15, 34 : 28, 35 : 9,
    36 : 8, 37 : 36, 38 : 18, 39 : 32, 40 : 17
};

num_maps[4] = {
    0 : 5, 1 : 20, 2 : 32, 3 : 26, 4 : 3, 5 : 38,
    6 : 4, 7 : 21, 8 : 13, 9 : 31, 10 : 17,
    11 : 30, 12 : 18, 13 : 23, 14 : 25, 15 : 28,
    16 : 14, 17 : 34, 18 : 16, 19 : 11, 20 : 40,
    21 : 10, 22 : 36, 23 : 6, 24 : 19, 25 : 15,
    26 : 12, 27 : 9, 28 : 2, 29 : 1, 30 : 33,
    31 : 35, 32 : 37, 33 : 29, 34 : 22, 35 : 39,
    36 : 7, 37 : 27, 38 : 24, 39 : 0, 40 : 8
}

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
/** ############################################### */

function constructRevNumMap(num_disk) {
    var rev_num_disk = {};
    for (var j in num_disk) {
        if (hasOwnProperty.call(num_disk, j)) {
            var val = num_disk[j];
            rev_num_disk[val] = j - 0;
        }
    }
    return rev_num_disk;
}

function constructRevCharMap(char_map) {
    var rev_char_map = {};
    for (var i in char_map) {
        if (hasOwnProperty.call(char_map, i)) {
            var val = char_map[i];
            rev_char_map[val] = i;
        }
    }
    return rev_char_map;
}

function initialize() {
    // Construct rev_num_maps from num_maps
    for (var i = 0; i < num_maps.length; i++) {
        rev_num_maps[i] = constructRevNumMap(num_maps[i]);
    }
    // Construct rev_char_map from char_map
    rev_char_map = constructRevCharMap(char_map);
}

/**
 *  getEncryptedCode:
 *      Encrypts the given string with "Feligma" Encryption Algorithm
 *  @param {String} [toEncrypt] the string to encrypt with Feligma Algorithm
 *
 *  @returns {String} Encoded string
 */
function getEncryptedCode(toEncrypt) {
    var encrypted_code = [];
    for (var i = 0; i < toEncrypt.length; i++) {
        var word = toEncrypt[i].toLowerCase();
        var code;
        if (word !== ' ') {
            var n = getCharCode(word);
            var output = encrypt(n);
            code = getChar(output);
        } else {
            code = ' ';
        }
        encrypted_code.push(code);
    }
    return encrypted_code.join('');
}

initialize();
console.log(getEncryptedCode(SECRET_WORD));
// console.log('Encrypted message (ignore quotes): \')fk~y+ &y{(@ &tqn!-\'');

// Hint: Secret word md5 signature: a78275598ed616d21a524787a573f9b7

import os
import sys

KEY_SIZE = 10

def expand_key(key, length):
	return (length / len(key)) * key + key[0:(length % len(key))]

def xor(s1, s2):
	assert len(s1) == len(s2)
	return ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(s1, s2)])

def main():
	if len(sys.argv) == 2:
		key = os.urandom(KEY_SIZE)

		filename = sys.argv[1]

		f = open(filename)
		data = f.read()
		f.close()

		expanded_key = expand_key(key, len(data))
		data_encrypted = xor(expanded_key, data)

		f = open(filename + ".enc", "w")
		f.write(data_encrypted)
		f.close()

		print "File %s encrypted with key: %s" % (filename, key.encode("hex"))
	else:
		print "Usage: %s <filename>" % (sys.argv[0])

if __name__ == "__main__":
	main()
#!/usr/bin/python

from Crypto.Cipher import AES
import numpy as np
import random
import sys
import time

# 0 is easy, 1 is moderate, 2 is hard
LEVEL = 0
print 'LEVEL (1-3):'
uinp = sys.stdin.readline().strip()
if uinp == '1':
  LEVEL = 0
elif uinp == '2':
  LEVEL = 1
elif uinp == '3':
  LEVEL = 2

FLAG = open('flag').read().split('\n')[LEVEL]
SECRET = None

N = 64
Q = 236
A = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131])

def R(choices):
  return choices[random.randint(0, len(choices) - 1)]

def chi(values=[-1,0,1]):
  return np.array([R(values) for _ in range(N)], dtype=np.int)

def X(a, b):
  am = np.fft.fft(a, 2*N)
  bm = np.fft.fft(b, 2*N)
  c = np.fft.ifft(am * bm).real
  return (c[:N] - c[N:]).astype(np.int)

class Client:
  def __init__(self):
    self.generate()

  def generate(self):
    self.secret = chi() % Q
    self.public = (X(A, self.secret) + chi([0])) % Q

  def output(self):
    return self.public

  def input(self, public):
    fixed = X(public, self.secret) % Q
    self.key = [0 if b<Q/2 else 1 for b in fixed]
    fixed = X(self.key, A) % Q
    self.verifier = [0 if b<Q/2 else 1 for b in fixed]

  def __str__(self):
    return ''.join('%02x' % i for i in np.packbits(self.key))

FAIL = 0

def establish():
  global SECRET, FAIL

  alice = Client()
  bob = Client()
  bob.input(alice.output())
  alice.input(bob.output())

  if alice.verifier != bob.verifier:
    FAIL += 1
    return None

  SECRET = str(alice)

  return (alice.output(), bob.output(), alice.verifier)

def encrypt(c):
  return AES.new(SECRET, AES.MODE_CBC, '\x00'*16).encrypt(c).encode('base64')

def decrypt(c):
  return AES.new(SECRET, AES.MODE_CBC, '\x00'*16).decrypt(c.decode('base64'))

if LEVEL < 2:
  random.seed(int(time.time()))

result = None
while result == None:
  result = establish()

(p1, p2, verifier) = result
verifier = ''.join('%02x' % i for i in np.packbits(verifier))
print 'PA: ' + ''.join('%02x' % i for i in p1)
print 'PB: ' + ''.join('%02x' % i for i in p2)
print 'VF: ' + verifier

if LEVEL < 1:
  print SECRET

if decrypt(raw_input('AES(VF, SECRET) = ')) == verifier:
  print FLAG
else:
  print encrypt(verifier)

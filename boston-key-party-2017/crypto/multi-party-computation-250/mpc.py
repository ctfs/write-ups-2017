from Crypto.Util import number
import random

from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

import sys
import json

import traceback

def L(x, n):
  return (x-1) // n


def paillier_keygen():
  # Returns (pk, sk)
  p = number.getStrongPrime(512)
  q = number.getStrongPrime(512)
  n = p*q
  lam = (p-1)*(q-1)/2
  while True:
    g = random.randrange(n**2)
    if number.GCD(g, n) != 1:
      continue
    mu_inv = L(pow(g, lam, n**2), n)
    if number.GCD(mu_inv, n) != 1:
      continue
    mu = number.inverse(mu_inv, n)
    break
  return (n, g), (lam, mu)

def paillier_encrypt((n, g), m):
  while True:
    r = random.randrange(n)
    if number.GCD(r, n) == 1:
      break
  return (pow(g, m, n**2) * pow(r, n, n**2)) % (n**2)

def paillier_decrypt((n, g), (lam, mu), c):
  return (L(pow(c, lam, n**2), n) * mu) % n

def paillier_add((n, g), a, b):
  return (a * b) % (n**2)

def paillier_multiply((n, g), a, k):
  return pow(a, k, n**2)

def mpc_monomial(point):
  return [-point, 1]

def mpc_multiply_poly(n, x, y):
  result = [0]*(len(x) + len(y))
  for i in range(len(x)):
    for j in range(len(y)):
      result[i+j] += (result[i+j] + x[i]*y[j]) % n
  return result

def mpc_encrypt_poly(pk, poly):
  return [paillier_encrypt(pk, term) for term in poly]

def mpc_client_genpoly((n, g), points):
  result = [1]
  for point in points:
    result = mpc_multiply_poly(n, result, mpc_monomial(point))
  return mpc_encrypt_poly(pk, result)

def mpc_evaluate_poly((n, g), poly, point):
  pow_point = point
  result = poly[0]
  for term in poly[1:]:
    result = paillier_add((n, g), result, paillier_multiply((n, g), term, pow_point))
    pow_point = (pow_point * point) % n
  return result

def mpc_server_side((n, g), poly, points):
  for point in points:
    result = mpc_evaluate_poly((n, g), poly, point)
    result = paillier_multiply((n, g), result, random.randrange(n))
    result = paillier_add((n, g), result, paillier_encrypt((n, g), point))
    yield result

def mpc_client_parseresults(pk, sk, c_points, s_points_enc):
  s_points = [paillier_decrypt(pk, sk, point) for point in s_points_enc]
  return set(c_points) & set(s_points)



class MpcHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    try:
      data_str = self.rfile.read(int(self.headers.getheader('content-length')))
      data = json.loads(data_str)
      n = data['n']
      if (n < 2**64):
        raise ValueError('too small')
      g = data['g']
      poly = data['poly']
      l = list(mpc_server_side((n, g), poly, POINTS))
      random.shuffle(l)
      result = json.dumps(l)
    except Exception as e:
      self.send_response(400)
    else:
      self.send_response(200)
      self.end_headers()
      self.wfile.write(result)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  pass

if __name__=="__main__":
  assert(len(sys.argv) >= 3)

  with open('FLAG.txt', 'r') as f:
    flag = f.read()[:-1]
  print flag

  POINTS = []
  for i in range(len(flag)):
    POINTS.append(random.randrange(2**48) * 256)
  POINTS.sort()
  for i in range(len(flag)):
    POINTS[i] += ord(flag[i])
  print POINTS

  server = ThreadedHTTPServer((sys.argv[1], int(sys.argv[2])), MpcHandler)
  server.serve_forever()


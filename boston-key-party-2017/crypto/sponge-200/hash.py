from Crypto.Cipher import AES
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import sys

class Hasher:
  def __init__(self):
    self.aes = AES.new('\x00'*16)

  def reset(self):
    self.state = '\x00'*16

  def ingest(self, block):
    """Ingest a block of 10 characters """
    block += '\x00'*6
    state = ""
    for i in range(16):
      state += chr(ord(self.state[i]) ^ ord(block[i]))
    self.state = self.aes.encrypt(state)

  def final_ingest(self, block):
    """Call this for the final ingestion.

    Calling this with a 0 length block is the same as calling it one round
    earlier with a 10 length block.
    """
    if len(block) == 10:
      self.ingest(block)
      self.ingest('\x80' + '\x00'*8 + '\x01')
    elif len(block) == 9:
      self.ingest(block + '\x81')
    else:
      self.ingest(block + '\x80' + '\x00'*(8-len(block)) + '\x01')

  def squeeze(self):
    """Output a block of hash information"""
    result = self.state[:10]
    self.state = self.aes.encrypt(self.state)
    return result

  def hash(self, s):
    """Hash an input of any length of bytes.  Return a 160-bit digest."""
    self.reset()
    blocks = len(s) // 10
    for i in range(blocks):
      self.ingest(s[10*i:10*(i+1)])
    self.final_ingest(s[blocks*10:])

    return self.squeeze() + self.squeeze()

class HashHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path in ['/favicon.ico', '/index.html']:
      # Stop.
      self.send_response(409)
      return

    try:
      to_hash = self.path[1:].decode('hex')
    except TypeError:
      # Bad hex.
      self.send_response(418)
      return

    if to_hash == GIVEN:
      # Nice try.
      self.send_response(451)
      return

    result = HASHER.hash(to_hash)
    if result != TARGET:
      # Wrong
      self.send_response(400)
      return
    self.send_response(200)
    self.end_headers()
    self.wfile.write(FLAG)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  pass

if __name__=='__main__':
  assert(len(sys.argv) >= 3)
  HASHER = Hasher()
  with open('FLAG.txt') as f:
    FLAG = f.read()
  GIVEN = 'I love using sponges for crypto'
  TARGET = HASHER.hash(GIVEN)
  server = ThreadedHTTPServer((sys.argv[1], int(sys.argv[2])), HashHandler)
  server.serve_forever()

import random
import string

def is_static_file(file):
  matches = ['/sites/default/files', '/themes/']
  if any(x in file for x in matches):
    return True
  else:
    return False

def random_string(length=8):
  random_string = ''.join(random.choices(string.ascii_letters, k=length))
  return str(random_string)


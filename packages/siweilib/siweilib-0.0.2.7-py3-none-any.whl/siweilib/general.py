# general utilities
import os
from itertools import chain
from termcolor import colored
import datetime
import pytz
import random
import subprocess
import copy
import pprint
import cryptography, cryptography.fernet
import string

######## FILE IO ########

def read_file(fpath):
  try:
    f = open(fpath, 'r')
    s = f.read()
    f.close()
    return s
  except Exception as e:
    # error message?
    return None

def write_file(fnom, s):
  f = open(fnom, 'w')
  f.write(s)
  f.close()

# most of the time you're gonna want to add '\n' to s
def append_file(fnom, s):
  f = open(fnom, 'a')
  f.write(s)
  f.close()

######## DATE SHIT ########

def str_to_date(date_str):
  return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def date_to_str(dat):
  return dat.strftime('%Y-%m-%d')

def unixtime_to_str(t):
  return datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def unixtime_to_str_in_timezone(t, tz_str):
  return datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.timezone('utc')).astimezone(pytz.timezone(tz_str)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def str_to_datetime_in_timezone(day_str, time_str, tz_str):
  tmp_time_obj = datetime.datetime.strptime(
      '%s %s' % (day_str, time_str), '%Y-%m-%d %H:%M:%S')
  return pytz.timezone(tz_str).localize(tmp_time_obj)

# compute the date of the start of the week...
def get_ws_from_ds(ds):
  date_obj = str_to_date(ds)
  weekday_num = date_obj.isocalendar()[2]
  start_of_week = date_obj - datetime.timedelta(days = weekday_num - 1)
  return date_to_str(start_of_week)

######## TERMINAL OUTPUT ########

def error_message(s):
  return colored(s, 'red', attrs=['bold'])

def ok_message(s):
  return colored(s, 'green', attrs=['bold'])

def highlight_message(s):
  return colored(s, 'yellow', attrs=['bold'])

def pp(s):
  return pprint.pprint(s)

######## MISC ########

def coalesce(a, b):
  if a is None:
    return b
  return a

def identity(x):
  return x

# listify a dict with the keys ordered...
def sort_dict(d):
  tmp = [(k, v) for k, v in d.items()]
  return sorted(tmp, key=lambda k: k[0])

######## CRYPTO ########

def generate_encryption_key():
  return cryptography.fernet.Fernet.generate_key()

def write_key(fnom, key):
  with open(fnom, 'wb') as f:
    f.write(key)

def read_key(fnom):
  f = open(fnom, 'rb')
  s = f.read()
  f.close()
  return s

def encrypt(plain_text, key):
  f = cryptography.fernet.Fernet(key)
  return f.encrypt(plain_text.encode()).decode()

def decrypt(cipher_text, key):
  f = cryptography.fernet.Fernet(key)
  return f.decrypt(cipher_text.encode()).decode()

def generate_random_string_unsecure(n = 8):
  return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

##################
# Tree libraries #
##################

# tree object
class tree(object):
  def __init__(self, child_nodes = {}):
    self.children = child_nodes

  def is_leaf(self):
    return len(self) == 0

  def __iter__(self):
    if not self.is_leaf():
      for v in chain(*map(iter, self.children.values())):
        yield v
    yield self

  def __len__(self):
    return len(self.children)

  # generic dfs: run a function on all nodes
  def dfs(self, node_func, agg_func):
    ret = node_func(self)
    if self.is_leaf():
      return node_func(self)
    for k, v in self.children.items():
      ret = agg_func(ret, v.dfs(node_func, agg_func))
    return ret
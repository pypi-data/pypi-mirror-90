import hashlib
import sys
import os


 def get_file(file):
    chunk_size = 1024
     md5 = hashlib.md5()
     with open(file,'r',encoding='utf-8') as fp:
         chunk = fp.read(chunk_size)
         if chunk:
             md5.update(chunk.encode())
             return md5.hexdigest()

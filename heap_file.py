
import os
import struct
import sys  
import json

# Heap data entry format [type][length][doc_id][tombstone][data]

class HeapFile: 
    
    def write(doc_id, data):
        # Write a document to the heap file
        with open('heap_file.bin', 'ab') as f:
            f.write(json.dumps(0x01).encode('utf-8'))  # Encoding type (1 = JSON)
            f.write(json.dumps(len(data)).encode('utf-8'))
            f.write(json.dumps(doc_id).encode('utf-8'))
            f.write(json.dumps(0x00).encode('utf-8'))  # Tombstone (0 = alive)
            f.write(json.dumps(data).encode('utf-8'))

    def read(offset):
        with open('heap_file.bin', 'rb') as f:
            f.seek(offset)
            encodingType = f.read(1)
            length = f.read(4)
            tombstone = f.read(1)
            doc_id = f.read(4)
            data = f.read(length).decode('utf-8')
            if tombstone == b'\x00':
                return json.loads(data)
        return None

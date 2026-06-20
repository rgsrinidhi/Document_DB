
import os
import struct
import sys  
import json

# Heap data entry format [type][length][doc_id][tombstone][data]

class HeapFile: 

    def __init__(self):
        self.heap_file = 'heap_file.bin'

    def write(self, doc_id, data):
        # Write a document to the heap file
        
        with open(self.heap_file, 'ab') as f:
            f.seek(0, 2)  # Move to the end of the file
            offset = f.tell()  # Get the current offset 
            f.write(struct.pack('B', 0x01))  # Encoding type (1 = JSON)
            serialised_data = json.dumps(data).encode('utf-8')
            f.write(struct.pack('I', len(serialised_data)))
            f.write(struct.pack('Q', doc_id))
            f.write(struct.pack('B', 0x01))  # Tombstone (1 = alive)
            f.write(serialised_data)
            return offset  # Return the offset where the document was written
            

    def read(self, offset):
        with open(self.heap_file, 'rb') as f:
            f.seek(offset)
            encodingType = struct.unpack('B', f.read(1))[0]
            length = struct.unpack('I', f.read(4))[0]
            doc_id = struct.unpack('Q', f.read(8))[0]
            tombstone = struct.unpack('B', f.read(1))[0]
            data = f.read(length).decode('utf-8')
            if tombstone == 0x01:  # If the document is not deleted
                result = {
                    'doc_id': doc_id,
                    'data': json.loads(data)
                }
                return result
        return None

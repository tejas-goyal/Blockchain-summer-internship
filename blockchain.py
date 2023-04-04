import hashlib
import os
from PyPDF2 import PdfFileReader

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()

class BlockChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, '01/01/2021', 'Genesis block', '0')

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def hash_pdf(file_path):
    with open(file_path, 'rb') as f:
        pdf = PdfFileReader(f)
        content = ''
        for i in range(0, pdf.getNumPages()):
            content += pdf.getPage(i).extractText()
        sha = hashlib.sha256()
        sha.update(content.encode('utf-8'))
        return sha.hexdigest()

def add_document(blockchain, file_path):
    index = len(blockchain.chain) + 1
    timestamp = str(datetime.now())
    pdf_hash = hash_pdf(file_path)
    new_block = Block(index, timestamp, pdf_hash, '')
    blockchain.add_block(new_block)
    print('Document added to blockchain with hash:', pdf_hash)

if __name__ == '__main__':
    blockchain = BlockChain()
    file_path = 'confidential_doc.pdf'
    add_document(blockchain, file_path)

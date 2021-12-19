import hashlib
import json
from datetime import datetime
from uuid import uuid4

class Block:
    def __init__(self, previous_block_hash, transaction_list):

        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = f"{'/'.join(transaction_list)}/{previous_block_hash}"
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.timestamp = datetime.now().timestamp()

        
class Blockchain:
    def __init__(self):
        self.chain = []
        self.generate_genesis_block()
        
    def generate_genesis_block(self):
        self.chain.append(Block("0", ['Genesis Block']))
        
    def new_block(self, transaction_list):
        previous_block_hash = self.head.block_hash
        self.chain.append(Block(previous_block_hash, transaction_list))
        
    def display_chain(self):
        for i in range(len(self.chain)):
            print(f"Data {i + 1}: {self.chain[i].block_data}")
            print(f"Hash {i + 1}: {self.chain[i].block_hash}")
            print(f"Timestamp {i + 1}: {self.chain[i].timestamp}\n")
            
    def verify_chain(self):
        curr = -1
        prev = -2
        
        while -prev <= len(self.chain):
            if self.chain[curr].block_hash != hashlib.sha256(self.chain[curr].block_data.encode()).hexdigest():
                print ("Block hash does not match block data in block " + curr)
                return False
                
            if self.chain[curr].block_data.split("/")[-1] != self.chain[prev].block_hash:
                print ("Previous hashes do not match in block " + curr)
                return False
            
            prev -= 1
            curr -= 1
            
        print ("Hashes verified")
        return True
    
    def new_transaction(self, sender, receiver, item, quantity):
        transaction = {
            "transactionId": str(uuid4()),
            "sender": sender,
            "receiver": receiver,
            "item": item,
            "quantity": quantity
        }
        
        return json.dumps(transaction)
        
    def wallet(self, wallet):
        items = {}
        
        for block in self.chain:
            transactions = block.block_data.split("/")
            for transaction in transactions:
                if transaction[0] != "{" or transaction[-1] != "}":
                    continue
                    
                transaction = json.loads(transaction)
                    
                if transaction["sender"] == wallet:
                    if transaction["item"] in items:
                        items[transaction["item"]] -= transaction["quantity"]
                    else:
                        items[transaction["item"]] = -transaction["quantity"]
                        
                if transaction["receiver"] == wallet:
                    if transaction["item"] in items:
                        items[transaction["item"]] += transaction["quantity"]
                    else:
                        items[transaction["item"]] = transaction["quantity"]

        return items
    
    def verify_transaction(self, transactionId):
        for block in reversed(self.chain):
            transactions = block.block_data.split("/")
            
            for transaction in transactions:
                if transaction[0] != "{" or transaction[-1] != "}":
                    continue

                transaction = json.loads(transaction)
                if transactionId == transaction["transactionId"]:
                    return True
            
        return False
    
    @property
    def head(self):
        return self.chain[-1]

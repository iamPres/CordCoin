import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.last_block = -2

        with open("blockchain.json") as file:
            self.blocks = json.load(file)
        with open("users.json") as file:
            self.users = json.load(file)
        with open("adv_config.json") as file:
            self.adv_config = json.load(file)

    def add_advertiser(self, name, amount):
        status = True
        if name not in self.adv_config:
            self.adv_config.update({
            name : {
            'amount' : amount,
            'reserved' : {}
            }
            })
        else:
            status = False

        return status

        with open("adv_config.json", "w") as file:
            json.dump(self.adv_config, file)

    def reserve_funds(self, user, amount, advertiser):
        status = True
        if advertiser in self.adv_config:
            if amount < self.adv_config[advertiser]['amount']:
                self.adv_config[advertiser]['reserved'].update({user:amount})
                with open("adv_config.json") as file:
                    json.dump(self.adv_config, file)
            else:
                status = False
        else:
            status = False

        return status

    def add_user(self, user):
        status = True
        if user not in self.users:
            self.users.update({user:0})
            with open("users.json", "w") as file:
                json.dump(self.users, file)
        else:
            status = False
        return status

    def root(self):
        self.add_transaction('server', 'server', 0)
        self.add_block(True, 1)

    def add_transaction(self, sender, recipient, amount):
        status = True
        if amount <= self.users[sender]:
            transaction = {
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount
            }

            self.users[transaction['sender']] -= amount
            self.users[transaction['recipient']] += amount

            self.current_transactions.append(transaction)
            self.last_block += 1
        else:
            status = False

        return status

    def add_block(self, proof, previous_hash):
        block = {
        'index' : len(self.blocks),
        'time' : time(),
        'transactions' : self.current_transactions,
        'proof' : proof,
        'previous_hash' : previous_hash
        }

        self.current_transactions = []
        self.blocks.append(block)

        with open("blockchain.json", "w") as file:
            json.dump(self.blocks, file)

        with open("users.json", "w") as file:
            json.dump(self.users, file)

        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

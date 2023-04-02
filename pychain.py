# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Step 1: Create a Record Data Class
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

# Step 2: Create a PyChain Class to contain the chain and relevant chain functions
class PyChain:
    def __init__(self, chain: List[Block]):
        self.chain = chain
        self.difficulty = 2

    def add_block(self, block):
        block.prev_hash = self.chain[-1].hash_block()
        block.creator_id = len(self.chain)
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]

            if curr_block.prev_hash != prev_block.hash_block():
                return False
            if not self._is_valid_proof(curr_block, self.difficulty):
                return False
        return True

    def _is_valid_proof(self, block, difficulty):
        return block.hash_block()[:difficulty] == "0" * difficulty

# Step 3: Modify the Existing Block Data Class to Store Record Data
@dataclass 
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)


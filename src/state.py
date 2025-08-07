import queue

# === Machine State ===
class MachineState:
    def __init__(self):
        self.registers = [b'\x00' * 32 for _ in range(256)]
        self.memory = {}  # memory[(slot, offset)] = value
        self.storage = {}
        self.call_value = 0
        self.balance = 0
        self.sender = b"\x00"*20
        self.transfers = queue.Queue()
    
    def get_storage(self):
        return self.storage
    def set_storage(self, storage):
        self.storage = storage

    def get_call_value(self):
        return self.call_value
    def set_call_value(self, call_value):
        self.call_value = call_value
    
    def get_balance(self):
        return self.balance
    def set_balance(self, balance):
        self.balance = balance

    def get_sender(self):
        return self.sender
    def set_sender(self, sender):
        self.sender = sender
    
    def add_transfer(self, address, amount):
        pass
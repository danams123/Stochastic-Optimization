class Customer:
    def __init__(self, id: str, entry_time: str, merchandise: str):
        self.id: int = int(id)
        self.entry_time: int = int(entry_time)
        self.merchandise: int = int(merchandise)
        self.receipts = []
        self.shopping: bool = False
        self.queue = None

    def get_id(self) -> int:
        return self.id

    def get_entry_time(self) -> int:
        return self.entry_time

    def get_shopping(self) -> bool:
        return self.shopping

    def get_merchandise(self) -> int:
        return self.merchandise

    def set_entry_time(self, entry_time: int) -> int:
        self.entry_time = entry_time

    def start_shopping(self, queue):
        self.shopping = True
        self.queue = queue

    def end_shopping(self):
        self.shopping = False
        self.queue = None

    def add_receipt(self, receipt):
        self.receipts.append(receipt)

from typing import Dict

class DotDict:
    def __init__(self, data: Dict):
        self.data = data
    
    def init(self, data: Dict):
        self.data = data

    def __getattr__(self, key):
        """Implement x.y access, only one level supported
        Sample:

        p = DotDict(data)
        p.fields
        p.messages
        p.total_results
        """
        try:
            return self.data[key]
        except KeyError:
            return None

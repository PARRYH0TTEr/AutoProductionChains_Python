
class EntityIDGenerator:
    
    def __init__(self):
        self.globalIdIterator = 0
        
        
    def GetID(self):
        Id = self.globalIdIterator
        
        self.globalIdIterator += 1
        
        return str(Id)
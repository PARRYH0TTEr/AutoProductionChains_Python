from draftsman.entity import new_entity
from Util.EntityIDGenerator import EntityIDGenerator


class NewEntityGenerator:
    
    def __init__(self):
        self.entityIdGeneratorInstance = EntityIDGenerator()
    
    def GetNewEntity(self, newEntityPrototype):
        newId = self.entityIdGeneratorInstance.GetID()
        
        #print(newId)
        
        tempEntity = new_entity(newEntityPrototype, id=newId)
        
        return tempEntity
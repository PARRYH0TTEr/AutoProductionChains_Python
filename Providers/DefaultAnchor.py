from draftsman.entity import new_entity
from draftsman.entity import Entity

class DefaultAnchor:
    
    name = "output"
    dependencies = []
    
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.ownPrototypes = self.InitOwnPrototypes()
        self.propagationAnchor = self.ownPrototypes[-1]
        
        
        
    def InitOwnPrototypes(self):
        ownPrototypesContainer = []
        
        # Index 0
        OutputChest = new_entity("wooden-chest")
        
        ownPrototypesContainer.append(OutputChest)
        
        return ownPrototypesContainer
    

    def AddPrototypesToBlueprint(self):
        for prototype in self.ownPrototypes:
            self.blueprint.entities.append(prototype)
            
            
    def SelectBuildOffset(self, offset):
        match offset:
            case "north":
                self.BuildNorth()
            
            case "south":
                self.BuildSouth()

            case "east":
                self.BuildEast()

            case "west":
                self.BuildWest()
                
                            
                
    def BuildNorth(self):
        
        self.AddPrototypesToBlueprint()
        
    
    def BuildSouth(self):
        
        self.AddPrototypesToBlueprint()
    
    
    def BuildEast(self):
        
        self.AddPrototypesToBlueprint()
        
    
    def BuildWest(self):
        
        self.AddPrototypesToBlueprint()
from draftsman.entity import new_entity
from draftsman.entity import Entity

from draftsman.prototypes import inserter
from draftsman.prototypes import transport_belt

from Util.InserterDirectionEnum import InserterDirectionEnum
from Util.TransportBeltDirectionEnum import TransportBeltDirectionEnum

from Util.NewEntityGenerator import NewEntityGenerator


class DefaultAnchor:
    
    name = "output"
    dependencies = []
    
    def __init__(self, blueprint, newEntityGenerator: NewEntityGenerator):
        self.blueprint = blueprint
        self.newEntityGenerator = newEntityGenerator
        self.ownPrototypes = self.InitOwnPrototypes()
        self.propagationAnchor = self.ownPrototypes[-1]
        
        
        
    def InitOwnPrototypes(self):
        ownPrototypesContainer = []
        
        # Index 0
        OutputChest = new_entity("wooden-chest")
        
        #OutputChest = self.newEntityGenerator.GetNewEntity("fast-inserter")
        
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
        
        # Since the wooden chest is the defaultAnchorPoint, we do not need to set its position relative to other objects in the blueprint
        
        # Inserter
        # self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'],
        #                                        self.ownPrototypes[0].tile_position['y'] - self.ownPrototypes[1].tile_height)
        # self.ownPrototypes[1].direction = InserterDirectionEnum.GetDirection("down")
        
        # # InputBelt
        # self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'],
        #                                        self.ownPrototypes[1].tile_position['y'] - self.ownPrototypes[2].tile_height)
        # self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("down")
        
        self.AddPrototypesToBlueprint()
        
    
    def BuildSouth(self):
        
        # Inserter
        # self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'],
        #                                        self.ownPrototypes[0].tile_position['y'] + self.ownPrototypes[0].tile_height)
        # self.ownPrototypes[1].direction = InserterDirectionEnum.GetDirection("up")
    
        # # InputBelt
        # self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'],
        #                                        self.ownPrototypes[1].tile_position['y'] + self.ownPrototypes[1].tile_height)
        # self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("up")
        
        self.AddPrototypesToBlueprint()
    
    
    def BuildEast(self):
        
        # Inserter
        # self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'] + self.ownPrototypes[0].tile_width,
        #                                        self.ownPrototypes[0].tile_position['y'])
        # self.ownPrototypes[1].direction = InserterDirectionEnum.GetDirection("left")
        
        # # InputBelt
        # self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'] + self.ownPrototypes[1].tile_width,
        #                                        self.ownPrototypes[1].tile_position['y'])
        # self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("left")
        
        self.AddPrototypesToBlueprint()
        
    
    def BuildWest(self):
        
        # Inserter
        # self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'] - self.ownPrototypes[1].tile_width,
        #                                        self.ownPrototypes[0].tile_position['y'])
        # self.ownPrototypes[1].direction = InserterDirectionEnum.GetDirection("right")
        
        # # InputBelt
        # self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'] - self.ownPrototypes[2].tile_width,
        #                                        self.ownPrototypes[1].tile_position['y'])
        # self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("right")
        
        self.AddPrototypesToBlueprint()
from Providers.CopperplateProvider import CopperplateProvider
from Util.InserterDirectionEnum import InserterDirectionEnum
from Util.TransportBeltDirectionEnum import TransportBeltDirectionEnum

from draftsman.entity import new_entity
from draftsman.entity import Entity

from typing import *

from draftsman.prototypes import inserter
from draftsman.prototypes import assembling_machine
from draftsman.prototypes import transport_belt

class CopperCableProvider:

    name = "coppercable"
    dependencies = [CopperplateProvider]

    def __init__(self, blueprint, anchor):
        self.blueprint = blueprint
        self.anchor: Entity = anchor
        self.ownPrototypes = self.InitOwnPrototypes()
        self.propagationAnchor = self.ownPrototypes[-1].id
        
        
    def InitOwnPrototypes(self):
        ownPrototypesContainer = []
        
        # Index 0 & 1 (output)
        
        FastInserter1: inserter = new_entity("fast-inserter")
        OutputBelt1: transport_belt = new_entity("transport-belt")
        OutputBelt2: transport_belt = new_entity("transport-belt")
        FastInserter2: inserter = new_entity("fast-inserter")
        
        # Index 2
        AssemMach11: assembling_machine = new_entity("assembling-machine-1")
        AssemMach11.recipe = "copper-cable"
        
        ownPrototypesContainer.append(FastInserter1)
        ownPrototypesContainer.append(OutputBelt1)
        ownPrototypesContainer.append(OutputBelt2)
        ownPrototypesContainer.append(FastInserter2)
        
        ownPrototypesContainer.append(AssemMach11)
        
        return ownPrototypesContainer
        
        
    
    # Simple function to loop over every prototype in ownPrototypes and adds it to the blueprint
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


    # Builds the structure north of the anchor
    def BuildNorth(self):
        
        # Output
        
        self.ownPrototypes[0].tile_position = (self.anchor.tile_position['x'],
                                               self.anchor.tile_position['y'] - self.ownPrototypes[0].tile_height)
        self.ownPrototypes[0].direction = InserterDirectionEnum.GetDirection("down")
        
        self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'],
                                               self.ownPrototypes[0].tile_position['y'] - self.ownPrototypes[1].tile_height)
        self.ownPrototypes[1].direction = TransportBeltDirectionEnum.GetDirection("down")
        
        self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'],
                                               self.ownPrototypes[1].tile_position['y'] - self.ownPrototypes[2].tile_height)
        self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("down")
        
        self.ownPrototypes[3].tile_position = (self.ownPrototypes[2].tile_position['x'],
                                               self.ownPrototypes[2].tile_position['y'] - self.ownPrototypes[3].tile_height)
        self.ownPrototypes[3].direction = InserterDirectionEnum.GetDirection("down")
        
        
        # Assembling machine 1 

        self.ownPrototypes[4].tile_position = (self.ownPrototypes[3].tile_position['x'],
                                               self.ownPrototypes[3].tile_position['y'] - self.ownPrototypes[4].tile_height)

        self.AddPrototypesToBlueprint()
        

    # Builds the structure south of the anchor
    def BuildSouth(self):
        
        # Output
        
        self.ownPrototypes[0].tile_position = (self.anchor.tile_position['x'],
                                               self.anchor.tile_position['y'] + self.anchor.tile_height)
        self.ownPrototypes[0].direction = InserterDirectionEnum.GetDirection("up")
        
        self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'],
                                               self.ownPrototypes[0].tile_position['y'] + self.ownPrototypes[0].tile_height)
        self.ownPrototypes[1].direction = TransportBeltDirectionEnum.GetDirection("up")
        
        self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'],
                                               self.ownPrototypes[1].tile_position['y'] + self.ownPrototypes[1].tile_height)
        self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("up")
        
        self.ownPrototypes[3].tile_position = (self.ownPrototypes[2].tile_position['x'],
                                               self.ownPrototypes[2].tile_position['y'] + self.ownPrototypes[2].tile_height)
        self.ownPrototypes[3].direction = InserterDirectionEnum.GetDirection("up")
        
        
        # Assembling machine 1 

        self.ownPrototypes[4].tile_position = (self.ownPrototypes[3].tile_position['x'],
                                               self.ownPrototypes[3].tile_position['y'] + self.ownPrototypes[3].tile_height)
        
        self.AddPrototypesToBlueprint()
        
        

    # Builds the structure east of the anchor
    def BuildEast(self):
        
        # Output
        
        self.ownPrototypes[0].tile_position = (self.anchor.tile_position['x'] + self.anchor.tile_width,
                                               self.anchor.tile_position['y'])
        self.ownPrototypes[0].direction = InserterDirectionEnum.GetDirection("left")
        
        self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'] + self.ownPrototypes[0].tile_width,
                                               self.ownPrototypes[0].tile_position['y'])
        self.ownPrototypes[1].direction = TransportBeltDirectionEnum.GetDirection("left")
        
        self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'] + self.ownPrototypes[1].tile_width,
                                               self.ownPrototypes[1].tile_position['y'])
        self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("left")
        
        self.ownPrototypes[3].tile_position = (self.ownPrototypes[2].tile_position['x'] + self.ownPrototypes[2].tile_width,
                                               self.ownPrototypes[2].tile_position['y'])
        self.ownPrototypes[3].direction = InserterDirectionEnum.GetDirection("left")
        
        
        # Assembling machine 1 

        self.ownPrototypes[4].tile_position = (self.ownPrototypes[3].tile_position['x'] + self.ownPrototypes[3].tile_width,
                                               self.ownPrototypes[3].tile_position['y'])
        
        self.AddPrototypesToBlueprint()

    # Builds the structure west of the anchor
    def BuildWest(self):
        
        # Output
        self.ownPrototypes[0].tile_position = (self.anchor.tile_position['x'] - self.ownPrototypes[0].tile_width,
                                               self.anchor.tile_position['y'])
        self.ownPrototypes[0].direction = InserterDirectionEnum.GetDirection("right")
        
        self.ownPrototypes[1].tile_position = (self.ownPrototypes[0].tile_position['x'] - self.ownPrototypes[1].tile_width,
                                               self.ownPrototypes[0].tile_position['y'])
        self.ownPrototypes[1].direction = TransportBeltDirectionEnum.GetDirection("right")
        
        self.ownPrototypes[2].tile_position = (self.ownPrototypes[1].tile_position['x'] - self.ownPrototypes[2].tile_width,
                                               self.ownPrototypes[1].tile_position['y'])
        self.ownPrototypes[2].direction = TransportBeltDirectionEnum.GetDirection("right")
        
        self.ownPrototypes[3].tile_position = (self.ownPrototypes[2].tile_position['x'] - self.ownPrototypes[3].tile_width,
                                               self.ownPrototypes[2].tile_position['y'])
        self.ownPrototypes[3].direction = InserterDirectionEnum.GetDirection("right")
        
        
        # Assembling machine 1 

        self.ownPrototypes[4].tile_position = (self.ownPrototypes[3].tile_position['x'] - self.ownPrototypes[4].tile_width,
                                               self.ownPrototypes[3].tile_position['y'])
        
        self.AddPrototypesToBlueprint()
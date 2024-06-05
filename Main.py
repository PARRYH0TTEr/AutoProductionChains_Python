from draftsman import utils
from draftsman.blueprintable import Blueprint
from draftsman.entity import new_entity
import json
import pyperclip
import sys
from treelib import Node, Tree
from typing import *

import time


# Custom classes/packages/namespaces below
from Providers.DefaultAnchor import DefaultAnchor
from Providers.CoalProvider import CoalProvider
from Providers.IronProvider import IronProvider
from Providers.IronplateProvider import IronplateProvider
from Providers.CopperProvider import CopperProvider
from Providers.CopperplateProvider import CopperplateProvider
from Providers.IronGearWheelProvider import IronGearWheelProvider
from Providers.AutomationSciencePackProvider import AutomationSciencePackProvider
from Util.NewEntityGenerator import NewEntityGenerator

#IMPORTANT 1.1 -> Add the sourcecode to Github. Get version control working (but do not remove old code,
#               -> might be worth to compare the two programs that generate the same blueprint to compare performance)



#IMPORTANT 2.1 -> Each provider should have a list of all the structures/processes that it contains
#               -> and then the Build<Dir> should just adjust the tile_position and direction of the objects.
#               -> We do this so that we can pass a specific structure and thereby specific tile_position
#               -> (which translates to an anchor point) for all subsequent structures/children


#          ->  




#TODO1.1 -> FIXME1.1


#TODO1.2 -> At the moment, denoting the rate at which the graph should provide the desired output does nothing.
#        -> Make it (somewhat) dynamic in choosing which it should use, perhaps by looking up the speed of each and selecting
#        -> based on the first substructure that meets the criteria


#TODO1.3 -> Implement a graph class that represents the "m-ary tree" that should be used to represent the graph
#        -> Look into using Graphviz






# Depending on the input, return the root-node structure
def SelectInitialStructure(init_struct):
    match init_struct:
        case "default":
            return DefaultAnchor
        case "coal":
            return CoalProvider
        case "iron-ore":
            return IronProvider
        case "copper-ore":
            return CopperProvider
        case "ironplate":
            return IronplateProvider
        case "copperplate":
            return CopperplateProvider
        case "irongearwheel":
            return IronGearWheelProvider
        case "automationsciencepack":
            return AutomationSciencePackProvider
        case _:
            # Should probably not return a string but rather a default empty class\
            #  to accommodate all other faulty inputs
            return "Invalid argument"



# For a given process, preemptively return if it does not contain dependencies,
#   otherwise loop through and add all of its dependencies to the tree and recursively call
#   this function on each of them
def AddNode(tree: Tree, parentNode_NODE):
    if (len(parentNode_NODE.data.dependencies) == 0):
        return
    else:
        for dependency in parentNode_NODE.data.dependencies:
            #FIXME1.1 -> Giving the anchor of the parent is incorrect here, fix once the prototype is working!
            #tempInstance = dependency(parentNode_NODE.data.blueprint, parentNode_NODE.data.ownPrototypes[-1], newEntityGenerator_globalInstance)
            
            tempInstance_NODE = tree.create_node(dependency.name, parent=parentNode_NODE.identifier, data=dependency)
            AddNode(tree, tempInstance_NODE)


# Simply returns a wooden-chest prototype as the initial anchor point
def GetDefaultAnchor():
    
    resultChest = new_entity("wooden-chest")
    return resultChest


def TestPrintTree(tree: Tree):
    rootNodeID = tree.root
    
    #print(tree.get_node(rootNodeID).data)
    print(tree.children(rootNodeID))
    
# Returns an ordered list of build directions
# The build directions are hand-picked such that the production chain primarly build in two
#   directions depending on whatever build direction was initially picked for the output node
def GetAvailableBuildDirections(parentBuildDirection) -> List[str]:
        match parentBuildDirection:
            case "north":
                return ["north", "west", "east"]
            case "south":
                return ["south", "west", "east"]
            case "east":
                return ["east", "north", "south"]
            case "west":
                return ["west", "north", "south"]
    

# Deprecated
# Assumes that the entity does exist in the blueprint
def FindEntityFromId(blueprint: Blueprint, entityId):
    entityList = blueprint.find_entities()
    print(entityList)
    for entity in entityList:
        if (entity.id == entityId):
            return entity



# Builds a production chain, based in the given "tree"
def BuildProductionChain(tree: Tree, nodeIdentifier, blueprint: Blueprint, nodeBuildDirection, parentAnchor, newEntityGenerator_globalInstance):
    #print(tree)
    #print(" ")
    
    # Get a node from its UUID
    treeNode: Node = tree.get_node(nodeIdentifier)

    # Enter this branch only once, when the current "treeNode" is the root of the tree
    # The root node does not have a parent, and thereby does not have some anchor point that it 
    #   needs to build from
    if (treeNode.is_root()):
        
        # Instantiate the current node (because the "tree" is build of classes and not objects)
        treeNode_ItemProvider_instance: DefaultAnchor = treeNode.data(blueprint, newEntityGenerator_globalInstance)
        
        # Add all the entities from this standalone circuit to the final blueprint
        treeNode_ItemProvider_instance.AddPrototypesToBlueprint()
        
        # Retrieve a list of build directions based on the build direction passed to this function
        # Unlike all child nodes, the root node does not have a parent, so a selected build direction
        #   was picked
        buildDirectionList = GetAvailableBuildDirections(nodeBuildDirection)
        
        # Retrieve a list of all child nodes
        treeNode_childList = tree.children(nodeIdentifier)
        
        # Loop over every child node, provide it with a build direction (from the 
        #   previously retrieved direction list), and recursively call this same function, with
        #   with the identifier of the child node
        for child in treeNode_childList:
    
            # Pop the head of the build direction list and save it for the recursive call
            #   on the child
            buildDirectionList_Head = buildDirectionList.pop(0)
            
            # Recurse with current child node and build direction in scope
            BuildProductionChain(tree, child.identifier, blueprint, buildDirectionList_Head, treeNode_ItemProvider_instance.ownPrototypes[-1], newEntityGenerator_globalInstance)
    
    # Enter this branch for all nodes that have a parent, aka all nodes except the parent node
    # The position of all these nodes is relative to where the location of the standalone circuit
    #   of their parent is
    else:
        #print(f"Adding {treeNode.tag} to blueprint")
        
        # Instantiate the current node (because the "tree" is build of classes and not objects)
        treeNode_ItemProvider_instance = treeNode.data(blueprint, parentAnchor, newEntityGenerator_globalInstance)
        
        # Build the current standalone circuit based on the build direction of the previous
        #   recursive call
        treeNode_ItemProvider_instance.SelectBuildOffset(nodeBuildDirection)
        
        # Retrieve a list of build directions based on the build direction passed to this function
        buildDirectionList = GetAvailableBuildDirections(nodeBuildDirection)
        
        # Retrieve a list of all child nodes
        treeNode_childList = tree.children(nodeIdentifier)
        
        # Loop over every child node, provide it with a build direction (from the 
        #   previously retrieved direction list), and recursively call this same function, with
        #   with the identifier of the child node
        for child in treeNode_childList:
            
            # Pop the head of the build direction list and save it for the recursive call
            #   on the child
            buildDirectionList_Head = buildDirectionList.pop(0)
                
            # Recurse with current child node and build direction in scope        
            BuildProductionChain(tree, child.identifier, blueprint, buildDirectionList_Head, treeNode_ItemProvider_instance.ownPrototypes[-1], newEntityGenerator_globalInstance)
        
        
        
        



def main():
    
    # Get start time for benchmarking
    start_time = time.perf_counter()

    # Initializing the blueprint
    newBlueprint = Blueprint()
    newBlueprint.label = "Test blueprints"


    newEntityGenerator_globalInstance = NewEntityGenerator()
        
    if len(sys.argv) > 3:
        # The first argument (sys.argv[0]) is the script name
        # The actual arguments start from sys.argv[1]
        arguments = sys.argv[1:]
        #print("Arguments passed:", arguments)

        # Extract the query-parameters
        queryAmount = sys.argv[1]
        queryOutput = sys.argv[2]
        queryRate = sys.argv[3]

        # Get the root node of the tree (and instantiate it)
        rootNode_default = SelectInitialStructure("default")#(newBlueprint, newEntityGenerator_globalInstance)
        
        lastProductionNode = SelectInitialStructure(queryOutput)#(newBlueprint, rootNode_default.ownPrototypes[-1], newEntityGenerator_globalInstance)



        # Instantiate a tree and add the rootnode to it
        tree = Tree()
        rootNode_NODE = tree.create_node(rootNode_default.name, parent=None, data=rootNode_default)
        
        
        lastProductionNode_NODE = tree.create_node(lastProductionNode.name, parent=rootNode_NODE.identifier, data=lastProductionNode)

        AddNode(tree, lastProductionNode_NODE)
        
        BuildProductionChain(tree, tree.root, newBlueprint, "north", (0,0), newEntityGenerator_globalInstance)
        
        output_string = newBlueprint.to_string()
        pyperclip.copy(output_string)
        
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        
        print(" ")
        print(f"It took {elapsed_time} to generate the production chain")
        print(" ")
        print("The blueprint string has been copied to your clipboard and is ready to be pasted into Factorio")
        
        #TestPrintTree(tree)

    else:
        print("Not enough arguments provided.")


if __name__ == "__main__":
    main()
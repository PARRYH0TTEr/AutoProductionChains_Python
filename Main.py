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
from Providers.CopperCableProvider import CopperCableProvider


#TODO1.2 -> At the moment, denoting the rate at which the graph should provide the desired output does nothing.
#        -> Make it (somewhat) dynamic in choosing which it should use, perhaps by looking up the speed of each and selecting
#        -> based on the first substructure that meets the criteria


#TODO1.3 -> Implement a graph class that represents the "m-ary tree" that should be used to represent the graph
#        -> Look into using Graphviz
#
#        -> 'treelib' provides a '.to_graphviz(...)' method that can convert a tree to a graph equivalent.

#TODO1.4 -> Build direction should be a command line argument






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
        case "coppercable":
            return CopperCableProvider
        case "automationsciencepack":
            return AutomationSciencePackProvider
        case _:
            # Return the default anchor, if the given outputType doesn't match any of the above (don't want a crash)
            return DefaultAnchor


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


# Builds a production chain, based in the given "tree"
def BuildProductionChain(tree: Tree, nodeIdentifier, blueprint: Blueprint, nodeBuildDirection, parentAnchor):
    #print(tree)
    #print(" ")
    
    # Get a node from its UUID
    treeNode: Node = tree.get_node(nodeIdentifier)

    # Enter this branch only once, when the current "treeNode" is the root of the tree
    # The root node does not have a parent, and thereby does not have some anchor point that it 
    #   needs to build from
    if (treeNode.is_root()):
        
        # Instantiate the current node (because the "tree" is build of classes and not objects)
        treeNode_ItemProvider_instance: DefaultAnchor = treeNode.data(blueprint)
        
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
            BuildProductionChain(tree, child.identifier, blueprint, buildDirectionList_Head, treeNode_ItemProvider_instance.ownPrototypes[-1])
    
    # Enter this branch for all nodes that have a parent, aka all nodes except the parent node
    # The position of all these nodes is relative to where the location of the standalone circuit
    #   of their parent is
    else:
        #print(f"Adding {treeNode.tag} to blueprint")
        
        # Instantiate the current node (because the "tree" is build of classes and not objects)
        treeNode_ItemProvider_instance = treeNode.data(blueprint, parentAnchor)
        
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
            BuildProductionChain(tree, child.identifier, blueprint, buildDirectionList_Head, treeNode_ItemProvider_instance.ownPrototypes[-1])
        
        
        
        



def main():
    
    if len(sys.argv) > 3:
        # The first argument (sys.argv[0]) is the script name
        # The actual arguments start from sys.argv[1]
        
        #print(sys.argv)
        
        arguments = sys.argv[1:]
        #print("Arguments passed:", arguments)

        # Extract the query-parameters
        queryAmount = sys.argv[1]
        queryOutput = sys.argv[2]
        queryRate = sys.argv[3]
        queryRunOrTest = sys.argv[4]



        if (queryRunOrTest == "-t"):
            
            # Initialize a runtime accumulator, so an average runtime 
            #   can be calculated later
            runTimeAccumulator = 0
            
            # 100 iterations is an arbitrary amount, but should result
            #   in a decently accurate average runtime
            #
            # Obviously an even larger amount of iterations would be better
            for i in range(100):
                
                start_time = time.perf_counter()

                # Initializing the blueprint
                newBlueprint = Blueprint()
                newBlueprint.label = f"Blueprint of {queryOutput} production chain"
                # Get the root node of the tree (and instantiate it)
                rootNode_default = SelectInitialStructure("default")#(newBlueprint, newEntityGenerator_globalInstance)
                
                lastProductionNode = SelectInitialStructure(queryOutput)#(newBlueprint, rootNode_default.ownPrototypes[-1], newEntityGenerator_globalInstance)

                # Instantiate a tree and add the rootnode to it
                tree = Tree()
                rootNode_NODE = tree.create_node(rootNode_default.name, parent=None, data=rootNode_default)
                
                # Have to create the child node of the final output, because the defaultAnchor does
                #   not have any providers in its dependency list
                lastProductionNode_NODE = tree.create_node(lastProductionNode.name, parent=rootNode_NODE.identifier, data=lastProductionNode)

                # Construct the n-ary tree
                AddNode(tree, lastProductionNode_NODE)
                
                # Build the production chain based on the constructed n-ary tree
                #
                # The (0,0) anchor point is just a default, not used value for the very first call to the function
                # 
                # Could probably just overload the function such a new definition without that anchor for the first call
                BuildProductionChain(tree, tree.root, newBlueprint, "south", (0,0))
                
                # Have to call .to_string() to get the blueprint string
                output_string = newBlueprint.to_string()
                
                # Just some util to automatically copy the above string to the clipboard
                pyperclip.copy(output_string)
                
                # Stop benchmark timer for this iteration
                end_time = time.perf_counter()
                
                # Calculate elapsed benchmark time
                elapsed_time = end_time - start_time
                
                runTimeAccumulator += elapsed_time
                
            runTimeAverage = (runTimeAccumulator / 100) * 1000
            
            print(" ")
            print(f"The average time it took to generate the production chain over 100 iterations was: {runTimeAverage} milliseconds")
            
            
        elif (queryRunOrTest == "-tverbose"):
            
            # Initialize a runtime accumulator, so an average runtime 
            #   can be calculated later
            runTimeAccumulator = 0
            
            # 100 iterations is an arbitrary amount, but should result
            #   in a decently accurate average runtime
            #
            # Obviously an even larger amount of iterations would be better
            for i in range(100):
                
                # Start benchmark timer for this iteration
                start_time = time.perf_counter()

                # Initializing the blueprint
                newBlueprint = Blueprint()
                newBlueprint.label = f"Blueprint of {queryOutput} production chain"
                # Get the root node of the tree (and instantiate it)
                rootNode_default = SelectInitialStructure("default")#(newBlueprint, newEntityGenerator_globalInstance)
                
                lastProductionNode = SelectInitialStructure(queryOutput)#(newBlueprint, rootNode_default.ownPrototypes[-1], newEntityGenerator_globalInstance)

                # Instantiate a tree and add the rootnode to it
                tree = Tree()
                rootNode_NODE = tree.create_node(rootNode_default.name, parent=None, data=rootNode_default)
                
                # Have to create the child node of the final output, because the defaultAnchor does
                #   not have any providers in its dependency list
                lastProductionNode_NODE = tree.create_node(lastProductionNode.name, parent=rootNode_NODE.identifier, data=lastProductionNode)

                # Construct the n-ary tree
                AddNode(tree, lastProductionNode_NODE)
                
                # Build the production chain based on the constructed n-ary tree
                #
                # The (0,0) anchor point is just a default, not used value for the very first call to the function
                # 
                # Could probably just overload the function such a new definition without that anchor for the first call
                BuildProductionChain(tree, tree.root, newBlueprint, "south", (0,0))
                
                # Have to call .to_string() to get the blueprint string
                output_string = newBlueprint.to_string()
                
                # Just some util to automatically copy the above string to the clipboard
                pyperclip.copy(output_string)
                
                # Stop benchmark timer for this iteration
                end_time = time.perf_counter()
                
                # Calculate elapsed benchmark time
                elapsed_time = end_time - start_time
                
                print("")
                print(f"The {i}-th generation of the {queryOutput} production chain took: {elapsed_time * 1000}")
                
                runTimeAccumulator += elapsed_time
                
            runTimeAverage = (runTimeAccumulator / 100) * 1000
            
            print(" ")
            print(f"The average time it took to generate the production chain over 100 iterations was: {runTimeAverage} milliseconds")
            
    
        elif (queryRunOrTest == "-r"):
            
            #start_time = time.perf_counter()

            # Initializing the blueprint
            newBlueprint = Blueprint()
            newBlueprint.label = f"Blueprint of {queryOutput} production chain"
            # Get the root node of the tree (and instantiate it)
            rootNode_default = SelectInitialStructure("default")#(newBlueprint, newEntityGenerator_globalInstance)
            
            lastProductionNode = SelectInitialStructure(queryOutput)#(newBlueprint, rootNode_default.ownPrototypes[-1], newEntityGenerator_globalInstance)

            # Instantiate a tree and add the rootnode to it
            tree = Tree()
            rootNode_NODE = tree.create_node(rootNode_default.name, parent=None, data=rootNode_default)
            
            # Have to create the child node of the final output, because the defaultAnchor does
                #   not have any providers in its dependency list
            lastProductionNode_NODE = tree.create_node(lastProductionNode.name, parent=rootNode_NODE.identifier, data=lastProductionNode)

            # Construct the n-ary tree
            AddNode(tree, lastProductionNode_NODE)
            
            # Build the production chain based on the constructed n-ary tree
            #
            # The (0,0) anchor point is just a default, not used value for the very first call to the function
            # 
            # Could probably just overload the function such a new definition without that anchor for the first call
            BuildProductionChain(tree, tree.root, newBlueprint, "south", (0,0))
            
            # Have to call .to_string() to get the blueprint string
            output_string = newBlueprint.to_string()
            
            # Just some util to automatically copy the above string to the clipboard
            pyperclip.copy(output_string)
            
            # Used to convert the tree to a graphviz format - only used for report
            #tree.to_graphviz(graph='graph')
            
            print(" ")
            print(f"The blueprint string for the {queryOutput} production chain has been copied to your clipboard and is ready to be pasted into Factorio")
            
            #TestPrintTree(tree)
            
        else:
            print("Incorrect run or test parameter given")

    else:
        print("Not enough arguments provided.")


if __name__ == "__main__":
    main()
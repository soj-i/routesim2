import copy
import json
from simulator.node import Node


'''
class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = []
        self.logging = logging.getLogger('Node %d' % self.id)
'''
class Distance_Vector_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.logging.debug("new node %d" % self.id)

        '''
        - initialization refers only to self and neighbors

        1. dictionary: node -> [dist, entire-path]
        2. dictionary: neighbor node -> [dist, entire-path]
        

        - create helper to implement bellman's
            2 updates - new dv, or direct links have been updated
                    - call bellman to recalculate distances
        '''
        self.self_dictionary = {self.id: [0,[self.id]]} # self_dictionary k: node_id v: nodes for path

        self.neighbor_dv_dictionary = {} # node_id :[cost, [path]]|
        self.links_to_neighbor = {} # (src,dst) : latency
        self.sequence_number = 0
        self.neighbor_sequence_numbers = {} # node_id : most recent seq

    # Return a string
    def __str__(self):
        '''
        is called to when the simulation wants to print a representation of the node's state for debugging.
        This is not essential, but it may be helpful to implement this function so that DUMP_NODE events print
        sensible information. This function should return a string.
        '''
        "Rewrite this function to define your node dump printout"
        return "A DV Node: " + str(self.id) + "\n"
        '''
        is called to when the simulation wants to print a representation of the node's state for debugging.
        This is not essential, but it may be helpful to implement this function so that DUMP_NODE events print
        sensible information. This function should return a string.
        '''
        "Rewrite this function to define your node dump printout"
        return "A DV Node: " + str(self.id) + "\n"

    # Fill in this function
    

    def link_has_been_updated(self, neighbor, latency):
        '''
        is called to inform you that an outgoing link connected to your node has just changed its properties. 
        It tells you that you can reach a certain neighbor (identified by an integer) with a certain latency. 
        In response, you may want to update your tables and send further messages to your neighbors. 
        This function does not have to return anything.
        '''
        link_candidate = frozenset((self, neighbor))
        # latency = -1 if delete a link
        if latency == -1:
            # remove link from links dictionary 
            self.links_to_neighbor.pop(link_candidate) # remove self-neighbor link
            self.neighbor_dv_dictionary.pop(neighbor) # remove from MY copy of neighbor's dv

        else:
            if link_candidate not in self.links_to_neighbor or self.links_to_neighbor[link_candidate] != latency: # link not in current set
                self.links_to_neighbor[link_candidate] = latency # or if link is present AND new latency, recalc own dv

                self.self_dictionary[neighbor] = [latency, [neighbor]] # update neighbor's cost in self dv
            
                # recalculate self dv(?)

            pass
    
    def recalculate_distance_vector(self):
        old_dv = copy.deepcopy(self.self_dictionary)

        for neighbor_node, dv in self.neighbor_dv_dictionary.items():
            for dst, (cost, full_path) in dv.items():
                new_cost =  cost + self.links_to_neighbor[frozenset((self,neighbor_node))]
                if dst not in self.self_dictionary or self.self_dictionary[dst][0] > new_cost:
                    self.self_dictionary[dst] = [new_cost, [self] + [full_path]]
        if old_dv != self.self_dictionary: # if any updates to optimal dv
            self.broadcast_to_neighbors()
    
    def broadcast_to_neighbors(self):
        message = {"seq_num": self.sequence_number, "dv": self.self_dictionary}
        self.sequence_number += 1
        json_message = json.dumps(message)
        self.send_to_neighbors(json_message)



    # Fill in this function
    def process_incoming_routing_message(self, m):
        '''
        is called when a routing message "m" arrives at a node. This message would have been sent by a neighbor
        (more about how to do that later). The message is a string. In response, you may send further routing messages 
        using self.send_to_neighbors or self.send_to_neighbor. You may also update your tables. 
        This function does not have to return anything.
        '''
        dict_message = json.loads(m) # json obj -> dict
        seq_num = dict_message["seq_num"] 
        neigh_dv = dict_message["dv"]

        neighbor = list(neigh_dv.keys())[0] # first key should be neighbor node (?)
        
        if neighbor not in self.neighbor_sequence_numbers or seq_num > self.neighbor_sequence_numbers[neighbor]:
            self.neighbor_sequence_numbers[neighbor] = seq_num #update neighbor's sq num
            self.neighbor_dv_dictionary[neighbor] = neigh_dv #update neighbor's dv

            self.recalculate_distance_vector() # recalc since update detected

    # Return a neighbor, -1 if no path to destination

    def get_next_hop(self, destination):
        '''
        is called when the simulator wants to know what your node currently thinks is the next hop on the 
        path to the destination node. You should consult your routing table or whatever other mechanism you
        have devised and then return the correct next node for reaching the destination.
        This function should return an integer.
        '''
        
        if destination in self.self_dictionary: #destination = { node : [cost , [path]}
            print(self.self_dictionary)
            path = self.self_dictionary[destination][1]
            
            if len(path) > 1: #
                return path[1]

        return 0 # error(?)

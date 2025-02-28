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
        self.self_dictionary = {self.id: [0, self.id]}

        self.neighbor_dictionary = {}

    # Return a string
    def __str__(self):
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
        # latency = -1 if delete a link
        if latency == -1:
            self.neighbor_dictionary.pop(neighbor)
        else:
            if neighbor not in self.neighbor_dictionary:
                self.neighbor_dictionary[neighbor] = [1, self.neighbor] 
            pass

    # Fill in this function
    def process_incoming_routing_message(self, m):
        '''
        is called when a routing message "m" arrives at a node. This message would have been sent by a neighbor
        (more about how to do that later). The message is a string. In response, you may send further routing messages 
        using self.send_to_neighbors or self.send_to_neighbor. You may also update your tables. 
        This function does not have to return anything.
        '''
        pass

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        '''
        is called when the simulator wants to know what your node currently thinks is the next hop on the 
        path to the destination node. You should consult your routing table or whatever other mechanism you
        have devised and then return the correct next node for reaching the destination.
        This function should return an integer.
        '''
        

        return -1

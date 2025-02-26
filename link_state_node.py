from simulator.node import Node

import json
# Link State psuedocode
'''
LINK STATE PSUEDOCODE
- controlled flooding --> nodes retransmit packet only 
the first time it is seen by a node.
* broadcast packages should have a unique id -- 
    to know if a node has already seen this information
* nodes must remember all recently seen message id

info we want to send: (link_src, link_dst, seq_num, cost)
    seq_num (similar to a version number)= to know what is the most updated information
    this is important, because items are received out of order, so we can't take the 'latest' 
    information as the most updated. Because maybe the 'updated' information arrives before the 
    'outdated' information.

The (link_src, link_dst and seq_num) can uniquely identify this 
    information. If we see the same three combination again, 
    then we know to disregard it.

Process. 
1. New link length updated between point A and B.
2. Say point A notices the new update first.
3. A sends out a broadcast message (A, B, 0, length = 3)
4. A will store this message. (everyone who receives also stores this message)
5. eventually A will get this message back, at this point the message can be ignored.

'''

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)

        self.last_message = []
        self.seq_num = 0

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        print("link updated, ", neighbor, ".")
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            # construct message to send.
            # append to the last message thing
            message = {[self.id, neighbor, self.seq_num]:[self.id, neighbor, latency, self.seq_num]}
            self.last_message.append(message)
            self.seq_num += 1
            # print("adding: ", self.id)
            print("this is last_message", self.last_message)
            # message = [self.id, neighbor, seq_num, latency]

    # Fill in this function
    def process_incoming_routing_message(self, m):
        print("new information", m, ".")

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        print("get_next_hop, ", destination)
        return -1

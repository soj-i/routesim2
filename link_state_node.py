from simulator.node import Node

import json
import heapq
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
# class Link():
#     def __init__(self, src: int, dst: int, cost: int):
#         self.src = src
#         self.dst = dst
#         self.seq_num = 0
#         self.cost = cost
    
#     def decode(self, m: str):
#         message = json.load(m)
    
    


class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.links = {}
        # self.seq_num = 0

    # Return a string
    def __str__(self):
        return "Rewrite this function to define your node dump printout"

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # latency = -1 if delete a link
        # print("link updated, ", neighbor, ".")
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            # add the new link to the link list
            message = {}

            if frozenset((self.id, neighbor)) in self.links: # if exists
                # print("Key 'a' exists")
                # print("Does exist", frozenset((self.id, neighbor)))
                seq_num = self.links[frozenset((self.id, neighbor))]["seq_num"]
                seq_num +=1 
                message = {"src": self.id, "dst": neighbor, "seq_num": seq_num, "cost": latency}
                self.links[frozenset((self.id, neighbor))] = message
                # print(self.links)

            else: # doesn't exist
                message = {"src": self.id, "dst": neighbor, "seq_num": 0, "cost": latency}

                # print("Does not exist ", frozenset((self.id, neighbor)))

                self.links[frozenset((self.id, neighbor))] = message
                # print(self.links)

            # turn into string
            s_message = json.dumps(message)
            # print("this is string message", s_message)
            self.send_to_neighbors(s_message)
            # print(self.links[frozenset((self.id, neighbor))])

            # self.last_message.append(message)
            # self.seq_num += 1
            # print("adding: ", self.id)
            # print("this is last_message", self.link)
            # message = [self.id, neighbor, seq_num, latency]

    # Fill in this function
    def process_incoming_routing_message(self, m):
        new_link = json.loads(m)
        # if incoming information exists in self.link and has a newer sequence number
        # or if information doesn't exist in self.link
        # then send to the other nodes.
        new_seq = new_link["seq_num"]
        new_src = new_link["src"]
        new_dst = new_link["dst"]
        new_cost = new_link["cost"]

        new_frozenset = frozenset((new_src, new_dst))

        if new_frozenset in self.links and new_seq > self.links[new_frozenset]["seq_num"] or new_frozenset not in self.links: # send to other nodes
            # print("send new information", new_link)
            # update self.links
            message = {"src": new_src, "dst": new_dst, "seq_num": new_seq, "cost": new_cost}
            self.links[new_frozenset] = message
            s_message = json.dumps(message)

            self.send_to_neighbors(s_message)
        # print("no new information", new_link, ".")

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        path, cost  = self.dijkstras(destination)
        if path is not None:
            print("this is what's returned", path)
            return path[0]
        # print("get_next_hop, ", destination)
        return -1

    def dijkstras(self, dst: int):
        print("THIS IS DEST, ", dst)
        graph = {}
        my_heap = []

        node_obj = {"src": self.id, "cost": 0, "path": []}

        s_obj = json.dumps(node_obj)

        heapq.heappush(my_heap, s_obj)

        # add source to the graph
        graph[self.id] = 0

        while len(my_heap) > 0:
            head = heapq.heappop(my_heap)

            l = json.loads(head)
            # print("this is head ,then l", head, l)

            h_id = l["src"]
            h_cost = l["cost"]
            h_path = l["path"]

            # print("this is id, cost, path", h_id, h_cost, h_path)
            # if the source is the destination
            if h_id == dst:
                return h_path, h_cost
            
            for link in self.links.items():
                
            #     print("this is link", link)
                link_src = link[1]["src"]
                link_dst = link[1]["dst"]
                link_seq = link[1]["seq_num"]
                link_cost = link[1]["cost"]

                print("this is src, dst, seq, cost", link_src, link_dst, link_seq, link_cost)

                if link_cost < 0:
                    pass
                else:
                    neighbor = None

                    if link_src == h_id:
                        neighbor = link_dst
                    elif link_dst == h_id:
                        neighbor = link_src
                    # print("whats goingon", neighbor)

            #         # if the neighbor is not None and the key is not already in the graph, or link_cost + h_cost less than the distance 
            #         # of the neighbor's path
                    if neighbor is not None:
                        if neighbor not in graph or link_cost + h_cost < graph[neighbor]:
                            print("neighbor added neighbor, link", neighbor, link, h_path)
                            
                            node_obj = {"src": neighbor, "cost": link_cost + h_cost, "path": h_path + [neighbor]}

                            s_obj = json.dumps(node_obj)

                            heapq.heappush(my_heap, s_obj)

            #                 #update the information in the graph
                            graph[neighbor] = link_cost + h_cost
                            print("link costs", link_cost+h_cost, graph)

        return None







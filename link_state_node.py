from simulator.node import Node

import json
import heapq
import math
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
class Links:
    def __init__(self, cost: int, seq_num: int):
        self.cost = cost
        self.seq_num = seq_num
    


class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.links = {}
        
        # self.seq_num = 0

    # Return a string
    def __str__(self):
        message = {}
        for fzset, mes in self.links.items():
            src = tuple(fzset)[0]
            dst = 0
            if src == self.id:
                dst = tuple(fzset)[1]
            else:
                src = tuple(fzset)[1]
                dst = tuple(fzset)[0]
            message[str((src, dst))] = mes
        m = json.dumps(message)
        return m
        

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        # print("         add_node")
        # latency = -1 if delete a link
        # print("link updated, ", neighbor, ".")
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
        else:
            # add the new link to the link list
            message = []

            if frozenset((self.id, neighbor)) in self.links: # if exists
                seq_num = self.links[frozenset((self.id, neighbor))][2]
                seq_num +=1 
                # message format: src, dst, seq_num, cost
                message = [self.id, neighbor, seq_num, latency]
                self.links[frozenset((self.id, neighbor))] = message
                # print(self.links)

            else: # doesn't exist
                message = [self.id, neighbor, 0, latency]

                self.links[frozenset((self.id, neighbor))] = message
            
            self.propagate()

            # # turn into string
            # # print("this is string message", s_message)
            # self.send_to_neighbors(s_message)
            # ge = set()
            # for neighbor in self.links.items():
            #     ge.add(neighbor[1]["src"])
            #     ge.add(neighbor[1]["dst"])
            # print("ge", ge)
            # for g in ge:
            #     self.send_to_neighbors(s_message)
    def propagate(self):
        message = {}
        for fzset, mes in self.links.items():
            src = tuple(fzset)[0]
            dst = 0
            if src == self.id:
                dst = tuple(fzset)[1]
            else:
                src = tuple(fzset)[1]
                dst = tuple(fzset)[0]
            message[str((src, dst))] = mes
        m = json.dumps(message)
        self.send_to_neighbors(m)

    # Fill in this function
    def process_incoming_routing_message(self, m):
        # print("         add_link")
        new_links = json.loads(m)
        need_to_update = False

        # loop through 
        for fzset, mes in new_links.items():
            s,d = fzset.split(',')
            s = int(s[1:])
            d = int(d[:-1])
            # frozenset((s,d))

            seq_num = mes[2]
            cost = mes[3]
            # print(seq_num, cost)

            new_frozenset = frozenset((s, d))
            if new_frozenset in self.links and seq_num > self.links[new_frozenset][2] or new_frozenset not in self.links:
                message = [s,d,seq_num,cost]
                self.links[new_frozenset] = message
                # update neighbors

                self.propagate()



        # #     print("link: ", fzset)
        # new_seq = new_link["seq_num"]
        # new_src = new_link["src"]
        # new_dst = new_link["dst"]
        # new_cost = new_link["cost"]
        # # self.links = new_links
        # # if incoming information exists in self.link and has a newer sequence number
        # # or if information doesn't exist in self.link
        # # then send to the other nodes.

        # new_frozenset = frozenset((new_src, new_dst))

        # if new_frozenset in self.links and new_seq > self.links[new_frozenset]["seq_num"] or new_frozenset not in self.links: # send to other nodes
        #     # print("send new information", new_link)
        #     # update self.links
        #     message = {"src": new_src, "dst": new_dst, "seq_num": new_seq, "cost": new_cost}
        #     self.links[new_frozenset] = message
        #     s_message = json.dumps(message)
        #     # print("THIS NODE: ", self.id, self.links)

        #     self.send_to_neighbors(s_message)
        #     ge = set()
        #     for neighbor in self.links.items():
        #         ge.add(neighbor[1]["src"])
        #         ge.add(neighbor[1]["dst"])
        #     for g in ge:
        #         self.send_to_neighbors(self.links)
        # # print("no new information", new_link, ".")

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        path, cost  = self.dijkstras(destination)
        if path is not None:
            print("this is what's returned", path)
            return path[0]
        # print("get_next_hop, ", destination)
        return -1
    
    def nnodes(self):
        numb = set()
        for _, mes in self.links.items():
            # print("THIS IS LINK", links)
            numb.add(mes[0])
            numb.add(mes[1])
        return len(numb), numb


    def dijkstras(self, dst: int):
        # print("THIS IS SRC, DST ", self.id, dst)
        my_heap = []
        len_nodes, unvisitednodes = self.nnodes()
        print("   Graph:", unvisitednodes)
        # visited = set()
        dist = {}
        prev = {}
        node_obj = [self.id, 0, []]
        heapq.heappush(my_heap, node_obj)
        # src, cost, path
        

        # for node in unvisitednodes:
        #     dist[node] = float('inf')
        #     prev[node] = None

        dist[self.id] = 0
        # visited.add(self.id)
        # neighbors = []

        while len(my_heap) > 0:
            minnode = heapq.heappop(my_heap)
            minnode_id = minnode[0]
            minnode_cost = minnode[1]
            minnode_path = minnode[2]

            if minnode_id == dst:
                return minnode_path, minnode_cost
            neighbors = []

            for fzset, mes in self.links.items():
                # print("this is link", fzset, mes)
                s = tuple(fzset)[0]
                d = tuple(fzset)[1]
                # frozenset((s,d))

                seq_num = mes[2]
                cost = mes[3]
            

                # print("this is src, dst, seq, cost", link_src, link_dst, link_seq, link_cost)
                
                if cost < 0:
                    pass
                else:
                    neighbor = None
                    if s == minnode_id:
                        # # print("only once")
                        # # if prev[link_src] != link_dst and [link_dst, link_cost] not in neighbors:
                        # # if link_dst not in visited and [link_dst, link_cost] not in neighbors:
                        # neighbors.append([link_dst, link_cost])
                        neighbor = d
                        # print("neighbors ",d )
                    elif d == minnode_id:
                        # print("only once")
                        # if prev[link_dst] != link_src and [link_src, link_cost] not in neighbors:
                        # if link_src not in visited and [link_src, link_cost] not in neighbors:
                        # neighbors.append([link_src, link_cost])
                        neighbor = s
                        print("neighbors ",s )
                        # visited.add(link_src)
                        # print("neighbors ", [link_src, link_cost] )
                    # print("whats goingon", neighbor)

                    if neighbor is not None:
                        # neighbors = sorted(neighbors, key=lambda x: x[1])
                        # print("lisf of neighbors [id, cost]", neighbors)
                        # visited.add(neighbor)
                        # neighbor = [id, link cost]
                        # for neighbor in neighbors: 
                        new_cost = cost + minnode_cost
                        if neighbor not in dist or new_cost < dist[neighbor]:
                            # print("costs: ", neighbor[1] + dist[minnode_id], "smaller than ", dist[neighbor[0]])
                            # print("neighbor added self.id, neighbor", self.id, neighbor )
                            # dist[neighbor[0]] = neighbor[1] + dist[minnode_id]
                            # prev[neighbor[0]] = minnode_id
                            # upate the heap
                            
                            node_obj = [neighbor, new_cost, minnode_path + [neighbor]]
                            # neighbors.append(node_obj)
                            # neighbors = sorted(neighbors, key=lambda x: x[1])

                            heapq.heappush(my_heap, node_obj)
                            my_heap = sorted(my_heap, key=lambda d: d[1])
                            # heapq.heappush(my_heap, )
                            # visited.add(neighbor[0])
                            # print("minnode pth", minnode_path)
                            dist[neighbor] = new_cost
                            # visited.add(neighbor)
                            
        
            # print("distances: [node, dist]", dist)
            # print("prev: [node, prevnode]", prev)
            # for node in dist.keys():
            #     if dist[node] == float('inf'): #disregard
            #         # print("some inf")
            #         continue
            #     path = []
            #     if node == self.id: # if this is the end, then end.
            #         # print("node == self.id", node, self.id)
            #         continue
            #     curr = node

            #     while curr != None:
            #         # path.insert(0, curr)
            #         # print("curr", curr)
            #         path.append(curr)
            #         curr = prev[curr]
            # path = path[::-1]
            # # print("path: ", path)
        return None

        #                 # src, cost, path
        #                 node_obj = [neighbor, link_cost + dist[minnode_id], h_path + [neighbor]]

        #                 heapq.heappush(my_heap, node_obj)

        #                 # my_heap = sorted(my_heap,key=self.keyfunc(node_obj))
        #                 my_heap = sorted(my_heap, key=lambda d: d[1])

        # #                 #update the information in the graph
        #                 graph[neighbor] = link_cost + graph[h_id]
                        
        #                 prev[neighbor] = h_id
        #                 # print("link costs", link_cost+h_cost, graph)
        #                 print("current graph", graph)
        #                 print("current prev: ", prev)
        #                 print("current heap: ", my_heap)
                    # 









import copy
import json

from simulator.node import Node

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
        self.self_dictionary = {} # self_dictionary k: node_id v: nodes for path

        self.neighbor_dvs = {}  # -> k: neighbor, v: DV_dict (k: dst: [cost, [path])

        self.neighbor_seq_nums = {} # node_id : most recent seq
        self.seq_num = 0
        self.link_costs = {} 

    # Return a string
    def __str__(self):
        '''
        is called to when the simulation wants to print a representation of the node's state for debugging.
        This is not essential, but it may be helpful to implement this function so that DUMP_NODE events print
        sensible information. This function should return a string.
        '''
        "Rewrite this function to define your node dump printout"
        message = {}
        for neighbor, dv in self.self_dictionary.items():
            message[neighbor] = {"cost": dv["cost"], "path": dv["path"]}

        message[-1] = self.seq_num
        self.seq_num += 1

        return copy.deepcopy(json.dumps(message))

    def link_has_been_updated(self, neighbor, latency):
        '''
        is called to inform you that an outgoing link connected to your node has just changed its properties. 
        It tells you that you can reach a certain neighbor (identified by an integer) with a certain latency. 
        In response, you may want to update your tables and send further messages to your neighbors. 
        This function does not have to return anything.
        '''
        # link_candidate = (self, neighbor)

        # latency = -1 if delete a link
        if latency == -1:
            # remove link from links dictionary 
            self.link_costs.pop(neighbor)
            self.neighbor_dvs.pop(neighbor)

        else:
            self.link_costs[neighbor] = latency

        self.recompute_dvs()

    def recompute_dvs(self):
        old_dvs = copy.deepcopy(self.self_dictionary)
        self.self_dictionary = {}

        for neighbor, link_cost in self.link_costs.items():
            self.self_dictionary[neighbor] = {"cost": link_cost, "path": [self.id, neighbor]}

        for source, dvs in self.neighbor_dvs.items():
            for destination, dv in dvs.items():
                self.recompute_single_dv(src=source, dst=destination, dv=dv)

        if self.self_dictionary != old_dvs:
            self.broadcast_to_neighbors()

    def recompute_single_dv(self, src: int, dst: int, dv: dict):
        if src not in self.link_costs:
            return
        new_cost = dv["cost"] + self.link_costs[src]
        if dst not in self.self_dictionary or (dst in self.self_dictionary and new_cost < self.self_dictionary[dst]["cost"]):
            new_path = [self.id] + copy.deepcopy(dv["path"])
            self.self_dictionary[dst] = {"cost": new_cost, "path": new_path}

    def broadcast_to_neighbors(self):
        self.send_to_neighbors(str(self))


    def process_incoming_routing_message(self, m):
        neighbor_self_dvs = json.loads(m)
        seq_num = neighbor_self_dvs['-1']

        del neighbor_self_dvs['-1']

        changed = False

        neighbor = int(neighbor_self_dvs[next(iter(neighbor_self_dvs))]['path'][0])
        to_delete = []
        if neighbor not in self.neighbor_dvs:
            self.neighbor_dvs[neighbor] = {}

        if neighbor in self.neighbor_seq_nums and seq_num < self.neighbor_seq_nums[neighbor]:
            return

        for dst, value in copy.deepcopy(self.neighbor_dvs[neighbor]).items():
            to_delete.append(dst)

        for dst_str, value in neighbor_self_dvs.items():
            dst = int(dst_str)
            if dst in to_delete:
                to_delete.remove(dst)

            link = {"cost": value["cost"], "path": value["path"]}

            changed = self.process_neighbor_dv(src=neighbor, dst=dst, dv=link, seq_num=seq_num) or changed

        for dst in to_delete:
            del self.neighbor_dvs[neighbor][dst]
            changed = True

        self.neighbor_seq_nums[neighbor] = seq_num

        if changed:
            self.recompute_dvs()

    def process_neighbor_dv(self, src, dst, dv, seq_num):
        if dst in self.neighbor_dvs[src]:
            if self.id in dv["path"]:
                del self.neighbor_dvs[src][dst]
                return True

            self.neighbor_dvs[src][dst] = dv
            return True
        else:
            if self.id in dv["path"]:
                return False
            else:
                self.neighbor_dvs[src][dst] = dv
                return True

    def get_next_hop(self, destination):
        # print("HELLOO")
        # print(self.self_dictionary)
        if destination in self.self_dictionary:
            if self.self_dictionary[destination]["cost"] < float('inf'):
                return copy.deepcopy(self.self_dictionary[destination]["path"])[1]

        return -1
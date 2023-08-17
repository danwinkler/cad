import numba
import numpy as np

class FastAgentSim:
    def __init__(self):
        self.agents = []
        self.data = []
        self.fns = {}

    def register_pairwise_function(self, name, fn):        
        
        #@numba.jit(numba.void(numba.float32[:,:]), nopython=True)
        @numba.jit(nopython=True)
        def apply(data):
            i = 0
            j = 0
            data_len = len(data)
            ret = []
            for i in range(data_len):
                first = True
                acc = None
                for j in range(data_len):
                    if i == j:
                        continue
                    
                    v = fn(data[i], data[j])

                    if first:
                        acc = v
                        first = False
                    else:
                        acc = acc + v
                ret.append(acc)
            
            return ret

        self.fns[name] = apply 

    def run_fn(self, name):
        fn = self.fns[name]
        fn(self.data)
    
    def add_agent(self, agent):
        self.agents.append(agent)
        self.data.append(agent.values)

class FastAgentField(object):
    def __init__(self, agent, index):
        self.agent = agent
        self.index = index
    
    def __get__(self, obj, objtype):
        return self.agent.values[self.index]
    
    def __set__(self, obj, value):
        self.agent.values[self.index] = value

class FastAgent(object):
    def create_fields(self, *field_names):
        self.values = np.array([0.0 for fn in field_names])
        self.next_values = np.copy(self.values)

        for i, field_name in enumerate(field_names):
            setattr(type(self), field_name, FastAgentField(self, i))

if __name__ == '__main__':
    import math
    import random
    class Node(FastAgent):
        def __init__(self, x, y):
            # Must be called first
            self.create_fields('x', 'y')

            self.x = x
            self.y = y

    @numba.jit(numba.float64[:](numba.float64[:], numba.float64[:]), nopython=True)
    def push(a, b):
        # TODO: it would be nice if we didn't have to unpack manually
        x1, y1, x2, y2 = a[0], a[1], b[0], b[1]
        dx = x2 - x1
        dy = y2 - y1
        d = math.sqrt(dx*dx + dy*dy)
        d = max(1, d)

        return np.array([dx / d, dy / d])

    fas = FastAgentSim()

    fas.register_pairwise_function('push', push)

    for i in range(10):
        n = Node(random.uniform(-100, 100), random.uniform(-100, 100))
        fas.add_agent(n)
    
    for i in range(100):
        fas.run_fn('push')

    
USAGE = """Naming convention:
    Nodes: V
    Edges: E
        Pairs of nodes: {v,w} (start_node, end_node)
        Maximum number of modules: maximum_number_of_modules
        Module cost: module_cost
        Single module capacity: single_module_capacity
            File:
            num_of_edges
            start_node end_node maximum_number_of_modules module_cost single_module_capacity
            ...
            -1
        
    Demands: D
        Pair of nodes: {o(d), t(d)}
        Demand volume (eg. Mbps): h(d)
        List of paths betweem o <-> d: P(d) = {P(d,1), P(d,2,...}
"""

USAGE = """Naming convention:
    Nodes: V
    Edges: E
        Pairs of nodes: {v,w}
        Modules: M
        Number of modules: epsilon(e)
        link.py capacity: C(e) 
    Demands: D
        Pair of nodes: {o(d), t(d)}
        Demand volume (eg. Mbps): h(d)
        List of paths betweem o <-> d: P(d) = {P(d,1), P(d,2,...}

File format:
    <network> ::= <links><EOL>-1<EOL><demands>

    <links>
        <number_of_links> ::= <integer>
        <list_of_links> 
            <link.py> ::= <start node> <end node> <numberof modules> <module cost> <link.py module>
    <demand>
        <number_of_demands> ::= <integer>
        <list_of_demands>
            <demand> ::= <start node> <end node> <demandvolume><EOL><demandpaths>
            <list_of_paths>
                <path> ::= <numberof demandpaths><EOL><demandpathlist>
                <list_of_demand_path_list>
                    <demandpath> ::= <demandpathid> <link.py list><EOL>
                    <link.py list> ::= <link.py id>[ <link.py id>]*
"""
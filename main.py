from helpers import CFG
from helpers import Graph

# helper function for get_strings()
def get_strings_helper(graph, start, end, cstr, strings, visited):
    if start == end:
        strings.append(cstr)
        return
    if start not in graph.adjacency_list:
        return
    visited.add(start)
    for (tgt, lbl) in graph.adjacency_list[start]:
        if tgt in visited:
            continue
        get_strings_helper(graph, tgt, end, cstr+lbl, strings, visited)
    visited.remove(start)

# return strings which lie along any path from a starting to ending vertex
def get_strings(graph, start, end):
    strings = []
    get_strings_helper(graph, start, end, "", strings, set())
    return strings
        
def check_reachability(cfg, graph, start_vertex, end_vertex):
    # TODO: Implement the function to check reachability
    graph_words = get_strings(graph, start_vertex, end_vertex)
    print(graph_words)
    return False

def read_input(file_path):
    with open(file_path, 'r') as file:
        num_inputs = int(file.readline().strip())
        inputs = []
        for _ in range(num_inputs):
            cfg_productions = file.readline().strip()
            graph_data = file.readline().strip()
            start_vertex = file.readline().strip()
            end_vertex = file.readline().strip()
            inputs.append((cfg_productions, graph_data, start_vertex, end_vertex))
        return inputs

def write_output(file_path, results):
    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')

def main(input_file, output_file):
    inputs = read_input(input_file)
    results = []
    for cfg_productions, graph_data, start_vertex, end_vertex in inputs:
        cfg = CFG(cfg_productions)
        graph = Graph()
        edge_data = graph_data.split(' ')
        for edge in edge_data:
            src = edge[0]
            dst = edge[1]
            label = edge[3]
            graph.add_edge(src, dst, label)
        print(cfg.parse_productions(cfg_productions))
        reachable = check_reachability(cfg, graph, start_vertex, end_vertex)
        results.append('Yes' if reachable else 'No')
    
    write_output(output_file, results)

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.txt'
    main(input_file, output_file)


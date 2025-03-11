from helpers import CFG, Graph


def cyk_algorithm(grammar: dict, word: str) -> bool:
    """
    Checks if a word can be generated by a given context-free grammar (CFG) using the Cocke-Younger-Kasami algorithm.
    Args:
        grammar: A dictionary representing the CFG. The keys are the variables and the values are lists of productions.
        word: A string representing the word to be checked.
    Returns:
        Boolean: True if the word can be generated by the grammar, False otherwise.
    """
    def combine_sets(set1, set2):
        result = set()
        if not set1 or not set2:
            return result
        for a in set1:
            for b in set2:
                result.add(a + b)
        return result

    # Splitting grammar into terminal and non-terminal rules
    non_terminals = []
    terminals = []

    # Extract non-terminal and terminal rules for conveniencd
    for var, productions in grammar.items():
        for prod in productions:
            if all(char.isupper() for char in prod[0]):
                non_terminals.append([var, prod[0]])
            else:
                terminals.append([var, prod[0]])

    n = len(word)
    non_term_vars = [nterm[0] for nterm in non_terminals]
    non_term_rules = [nterm[1] for nterm in non_terminals]

    # Initialize CYK table
    table = [[set() for _ in range(n - i)] for i in range(n)]

    # Fill table for single character matches
    for i in range(n):
        for terminal in terminals:
            if word[i] == terminal[1]:
                table[0][i].add(terminal[0])

    # Fill the rest of the table
    for length in range(1, n):
        for start in range(n - length):
            for partn in range(length):
                combined = combine_sets(table[partn][start], table[length - partn - 1][start + partn + 1])
                for item in combined:
                    if item in non_term_rules:
                        table[length][start].add(non_term_vars[non_term_rules.index(item)])

    # Check if start symbol 'S' can generate the word
    return 'S' in table[n - 1][0]

    

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
    for word in graph_words:
        possible = cyk_algorithm(cfg, word)
        if possible:
            return True
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
        reachable = check_reachability(cfg.parse_productions(cfg_productions), graph, start_vertex, end_vertex)
        results.append('Yes' if reachable else 'No')
    
    write_output(output_file, results)

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.txt'
    main(input_file, output_file)


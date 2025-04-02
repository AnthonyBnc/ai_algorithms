# Level 0: A -> Max
# 
# Level 1: B C D -> Min
# 
# Level 2: E - J -> Max
# 
# Level 3: K - V -> Leaf nodes (values)
# 

# Minimax Algorithm
# 1. Start at the root node
# 2. If the node is a max node, choose the child with the highest value
# 3. If the node is a min node, choose the child with the lowest value
# 4. Repeat until the leaf nodes are reached
# 5. Return the value of the leaf node

tree = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': ['G', 'H'],
    'D': ['I', 'J'],
    'E': [1, 5],   # K, L
    'F': [9, 3],   # M, N
    'G': [9, 7],   # O, P
    'H': [8, 7],   # Q, R
    'I': [2, 3],   # S, T
    'J': [5, 6],   # U, V
}

print("Task 1(a): Layers of the tree")
print("Level 0: A (MAX)")
print("Level 1: B C D (MIN)")
print("Level 2: E F G H I J (MAX)")
print("Level 3: K L M N O P Q R S T U V (LEAF)")


# Task 1(b): Minimax Algorithm
print("\nTask 1(b): Minimax Algorithm")
def minimax(node, is_maximizing, depth = 0):
    indent = " " * depth
    if isinstance (node, list):
        val = max(node) if is_maximizing else min(node)
        print(f"{indent}Leaf {node} → {'MAX' if is_maximizing else 'MIN'} returns {val}")
        return val
    
    print(f"{indent}{'MAX' if is_maximizing else 'MIN'} at node {node}")
    values = []
    for child in tree[node]:
        val = minimax(child, not is_maximizing, depth + 1)
        values.append(val)

    result = max(values)  if is_maximizing else min(values)
    print(f"{indent}{'MAX' if is_maximizing else 'MIN'} at node {node} returns {result}")
    return result
    
# Task 1(c): Alpha-Beta Pruning
def alphabeta(node, alpha, beta, is_maximizing, depth = 0):
    indent = " " * depth
    if isinstance(node, list):
        val = max(node) if is_maximizing else min(node)
        print(f"{indent}Leaf {node} → {'MAX' if is_maximizing else 'MIN'} returns {val}")
        return val
    
    
    print(f"{indent}{'MAX' if is_maximizing else 'MIN'} at node {node}")
    value = float('-inf') if is_maximizing else float('inf')

    for child in tree[node]:
        child_value = alphabeta(child, alpha, beta, not is_maximizing, depth + 1)
        if is_maximizing:
            value = max(value, child_value)
            alpha = max(alpha, value)
        else: 
            value = min(value, child_value)
            beta = min (beta, value)

        if beta <= alpha:
            print(f"{indent}Alpha-Beta Pruning at node {node}")
            break

    print(f"{indent}{'MAX' if is_maximizing else 'MIN'} at node {node} returns {value}")
    return value

# 1(d): Order of node examination 
visited_leaves = []

def trace_minimax(node, is_maximizing):
    if isinstance(node, list):
        visited_leaves.extend(node)
        return max(node) if is_maximizing else min(node)
    return max([trace_minimax(child, not is_maximizing) for child in tree[node]]) if is_maximizing else min([trace_minimax(child, not is_maximizing) for child in tree[node]])

print("\nTask 1(d): Order of node examination")
print("Minimax: ", end="")
result = trace_minimax('A', True)
print(f"Result: {result}")

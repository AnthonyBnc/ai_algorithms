reordered_tree = {
    'A': ['B', 'C', 'D'],
    'B': [12, 3],
    'C': [8, 10],
    'D': [5,14],
}

def alphabeta_reordered(node, alpha, beta, is_maximizing, depth = 0):
    indent = " " * depth
    if isinstance(node, list):
        val = max(node) if is_maximizing else min(node)
        print(f"{indent}Leaf {node} → {'MAX' if is_maximizing else 'MIN'} returns {val}")
        return val

    print(f"{indent}{'MAX' if is_maximizing else 'MIN'} at node {node}")
    value = float('-inf') if is_maximizing else float('inf')
    
    for child in reordered_tree[node]:
        child_val = alphabeta_reordered(child, alpha, beta, not is_maximizing, depth + 1)
        if is_maximizing: 
            value = max(value, child_val)
            alpha = max(alpha, value)
        else:
            value = min(value, child_val)
            beta = min(beta, value)
        
        if beta <= alpha:
            print(f"{indent} Pruned ramianign childe ata node {node}")
            break 
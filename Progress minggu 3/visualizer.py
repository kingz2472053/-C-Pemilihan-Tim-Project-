import matplotlib.pyplot as plt
import graphviz
from itertools import combinations
import time
from models import Candidate
from algorithm import BranchAndBound

def build_graphviz_tree(tree_nodes, candidates, max_nodes=100):
    dot = graphviz.Digraph(comment='Branch and Bound Tree')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', fontsize='10')
    dot.attr('edge', fontname='Helvetica', fontsize='9')
    
    count = 0
    for node in tree_nodes:
        if count >= max_nodes:
            break
        count += 1
        
        # Format label
        label_parts = []
        team_str = node.label if node.label else "root"
        label_parts.append(f"Team: {team_str}")
        cost_str = f"Rp {node.total_cost:,}".replace(',', '.')
        lb_str = f"Rp {node.lower_bound:,}".replace(',', '.')
        label_parts.append(f"Cost: {cost_str}")
        label_parts.append(f"LB: {lb_str}")
        
        # Color based on status
        if node.is_solution:
            color = "#d4edda" # green
            border = "#28a745"
            status = "OPTIMAL"
        elif node.pruned:
            color = "#f8d7da" # red
            border = "#dc3545"
            status = "PRUNED"
        else:
            color = "#cce5ff" # blue
            border = "#007bff"
            status = "ACTIVE"
            
        label_parts.append(f"Status: {status}")
        
        node_label = "\\n".join(label_parts)
        dot.node(str(node.node_id), node_label, fillcolor=color, color=border)
        
        if node.parent_id is not None:
            dot.edge(str(node.parent_id), str(node.node_id))
            
    if len(tree_nodes) > max_nodes:
        dot.node("...", f"... {len(tree_nodes) - max_nodes} nodes hidden", fillcolor="#e2e3e5", color="#6c757d")
        # connect to the last node just to show it
        # dot.edge(str(tree_nodes[max_nodes-1].node_id), "...")
        
    return dot

def brute_force_solve(candidates, k, B):
    best = None
    t0 = time.perf_counter()
    for combo in combinations(range(len(candidates)), k):
        total = sum(candidates[i].cost for i in combo)
        if total <= B and (best is None or total < best):
            best = total
    elapsed = time.perf_counter() - t0
    return best, elapsed

def plot_benchmark(candidates, k, B):
    # Run Branch and Bound
    bb = BranchAndBound(candidates, k, B)
    res_bb = bb.solve()
    bb_time = res_bb.elapsed_sec * 1000 # ms
    
    # Run Brute Force
    # WARNING: Brute force can be very slow for n > 25.
    # We will cap it to avoid freezing the app.
    if len(candidates) > 24:
        bf_time = 0
        bf_label = "Brute Force (Skipped > 24)"
    else:
        _, bf_sec = brute_force_solve(candidates, k, B)
        bf_time = bf_sec * 1000
        bf_label = "Brute Force"
        
    fig, ax = plt.subplots(figsize=(8, 5))
    methods = ['Branch & Bound', bf_label]
    times = [bb_time, bf_time]
    
    colors = ['#28a745', '#dc3545']
    bars = ax.bar(methods, times, color=colors)
    
    ax.set_ylabel('Execution Time (ms)')
    ax.set_title(f'Performance Comparison (n={len(candidates)}, k={k})')
    
    # Add value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            ax.text(bar.get_x() + bar.get_width()/2, yval + (max(times)*0.01), 
                    f'{yval:.2f} ms', ha='center', va='bottom', fontweight='bold')
            
    return fig

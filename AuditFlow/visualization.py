import networkx as nx
import matplotlib.pyplot as plt

def visualize_flow(df):
    if not hasattr(df, '_auditflow_tracker'):
        raise ValueError("The dataframe doesn't have tracing information.")
    
    G = nx.DiGraph()
    graph_data = df._auditflow_tracker.get_graph_data()

    # Define node shapes, sizes, and labels
    node_shapes = {}
    node_sizes = {}
    node_labels = {}

    final_node = None  # To store the final DataFrame node

    for node in graph_data['nodes']:
        if "result" in node:  # Assuming final DataFrame node contains 'result'
            node_shapes[node] = 's'  # Square for DataFrames
            node_sizes[node] = 3000  # Larger size for final DataFrame
            node_labels[node] = node  # Label the DataFrame node
            final_node = node  # Mark this as the final node
        elif "input" in node:  # Regular DataFrames
            node_shapes[node] = 's'
            node_sizes[node] = 2500
            node_labels[node] = node
        else:  # Operation nodes
            node_shapes[node] = 'o'
            node_sizes[node] = 1500
            node_labels[node] = node

        G.add_node(node)

    for edge in graph_data['edges']:
        G.add_edge(edge[0], edge[1])

    # Use shell layout for a more organized structure
    pos = nx.shell_layout(G)
    plt.figure(figsize=(12, 8))

    # Separate nodes into circles and squares
    df_nodes = [node for node in G.nodes if node_shapes[node] == 's']
    op_nodes = [node for node in G.nodes if node_shapes[node] == 'o']

    # Highlight final node differently (e.g., in red)
    final_node_color = 'red' if final_node else 'skyblue'

    # Draw DataFrame nodes as squares and operation nodes as circles
    nx.draw_networkx_nodes(G, pos, nodelist=df_nodes, node_shape='s', node_color='skyblue', 
                           node_size=[node_sizes[node] for node in df_nodes], alpha=0.9)
    


    nx.draw_networkx_nodes(G, pos, nodelist=op_nodes, node_shape='o', node_color='lightgreen', 
                           node_size=[node_sizes[node] for node in op_nodes], alpha=0.8)

    # Draw edges with arrows and adjustable arrow size
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20)

    # Label the nodes with their names
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8, font_color='black')

    # Remove axis and set title
    plt.title("Dataframe Transformation Flow")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

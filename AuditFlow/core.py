import pandas as pd
from functools import wraps

class OperationTracker:
    def __init__(self):
        self.nodes = set()
        self.edges = []
        self.data_info = {}  # To store information about DataFrames (input/output)

    def add_node(self, node, df):
        """
        Add a node and store the DataFrame info.
        """
        self.nodes.add(node)
        self.data_info[node] = {
            'shape': df.shape,
            'columns': list(df.columns),
            # You can add more information here like dtypes, memory usage, etc.
        }

    def add_edge(self, from_node, to_node, operation):
        self.edges.append((from_node, to_node, operation))

    def get_graph_data(self):
        return {
            'nodes': list(self.nodes),
            'edges': self.edges,
            'data_info': self.data_info  # Return DataFrame information for nodes
        }

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Initialize trackers for input DataFrames
        for arg in args:
            if isinstance(arg, pd.DataFrame):
                if not hasattr(arg, '_auditflow_name'):
                    arg._auditflow_name = f"input_{func.__name__}"
                if not hasattr(arg, '_auditflow_tracker'):
                    arg._auditflow_tracker = OperationTracker()
                # Store input DataFrame information
                arg._auditflow_tracker.add_node(arg._auditflow_name, arg)

        result = func(*args, **kwargs)
        
        if isinstance(result, pd.DataFrame):
            if not hasattr(result, '_auditflow_name'):
                result._auditflow_name = f"{func.__name__}_result"
            if not hasattr(result, '_auditflow_tracker'):
                result._auditflow_tracker = OperationTracker()
            
            # Store output DataFrame information
            result._auditflow_tracker.add_node(result._auditflow_name, result)
            
            for arg in args:
                if isinstance(arg, pd.DataFrame) and hasattr(arg, '_auditflow_name'):
                    result._auditflow_tracker.add_edge(
                        arg._auditflow_name, 
                        result._auditflow_name, 
                        func.__name__
                    )
                    # Update the new result tracker with the previous tracker's nodes and edges
                    result._auditflow_tracker.nodes.update(arg._auditflow_tracker.nodes)
                    result._auditflow_tracker.edges.extend(arg._auditflow_tracker.edges)
        return result
    return wrapper

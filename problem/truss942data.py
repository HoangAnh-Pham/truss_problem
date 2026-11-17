# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 15:04:21 2025

@author: Lenovo
"""

import numpy as np
import pandas as pd

class TrussData942:
    """Class to store all global data for 942-bar truss optimization"""
    def __init__(self):
        self.nvars = None
        self.XV = None
        self.XB = None
        self.NoN = None
        self.NoE = None
        self.Node = None
        self.Ele = None
        self.Mat = None
        self.Eleload = None
        self.NoD = None
        self.EleID = None
        self.ro = None
        self.E = None
        self.fy = None
        self.dm = None
        self.Nodeload = None
        self.lcase = None

def truss942data(excel_file='26StoreyTruss.xls', lcase=3):
    """
    942-bar 3D truss optimization problem
    
    Parameters:
    excel_file: path to Excel file containing truss data
    lcase: load case number (0-4)
    
    Returns:
    data: TrussData942 object containing all truss data
    """
    
    # Create global data object
    data = TrussData942()
    
    data.lcase = lcase
    data.nvars = 59
    
    # Material properties
    data.ro = 0.1    # lb/in^3
    data.E = 10000   # ksi
    data.fy = 25     # ksi
    data.dm = 15     # in
    A = 1
    I = 1
    
    # Load geometry data from Excel file
    try:
        # Read Excel file with multiple sheets
        excel_data = pd.ExcelFile(excel_file)
        
        # Read different sheets based on available data
        # Note: You may need to adjust sheet names based on actual Excel file structure
        if 'nodes1' in excel_data.sheet_names:
            nodes_df = pd.read_excel(excel_file, sheet_name='nodes1')
            elements_df = pd.read_excel(excel_file, sheet_name='elements1')
            loads_df = pd.read_excel(excel_file, sheet_name='external_loads')
        else:
            # Try alternative sheet names
            nodes_df = pd.read_excel(excel_file, sheet_name=0)  # First sheet
            elements_df = pd.read_excel(excel_file, sheet_name=1)  # Second sheet
            loads_df = pd.read_excel(excel_file, sheet_name=2)  # Third sheet
        
        # Extract node coordinates (all values in Excel are in ft)
        node = nodes_df.values
        Node0 = node[1:, 1:]  # Remove first column (node IDs), keep coordinates in ft
        data.Node = Node0 * 12  # Convert ft to inches
        
        # Extract element connectivity
        ele = elements_df.values
        data.Ele = ele[2:, 1:4].astype(int)  # Remove first column, keep connectivity
        
        # Correct the data (as in original MATLAB code)
        data.Ele[890:894, 1] = [227, 221, 232, 226]  # 0-based indexing adjustment
        
        data.NoN = len(data.Node)
        data.NoE = len(data.Ele)
        
        # Cross-section areas
        material_props = np.array([data.E, A, I, data.ro])
        data.Mat = np.kron(material_props, np.ones((data.nvars, 1)))
        
        # Loading
        load = loads_df.values
        load0 = np.zeros((data.NoN+1, 4))
        
        # for i in range(data.NoN):
        #     load0[i, 0] = i + 1  # Node number (1-based)
        #     load0[i, 1] = load[3*i, 3]     # X-load (4th column, 0-based index 3)
        #     load0[i, 2] = load[3*i + 1, 3] # Y-load
        #     load0[i, 3] = load[3*i + 2, 3] # Z-load
        
        # Load case selection
        if lcase == 0:
            data.Nodeload = load0
        elif lcase == 1:
            loads1_df = pd.read_excel(excel_file, sheet_name='loads1')
            data.Nodeload = loads1_df.values
        elif lcase == 2:
            # Py=1 kip at all nodes
            loads2_df = pd.read_excel(excel_file, sheet_name='loads2')
            data.Nodeload = loads2_df.values
        elif lcase == 3:
            # Px=1.5/1.0 kip at all left/right nodes
            loads3_df = pd.read_excel(excel_file, sheet_name='loads3')
            data.Nodeload = loads3_df.values
        elif lcase == 4:
            # Px=1.5/1.0 kip at all left/right nodes (including center nodes)
            loads4_df = pd.read_excel(excel_file, sheet_name='loads4')
            data.Nodeload = loads4_df.values
            
        data.Nodeload = data.Nodeload[1:,:]
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        print("Creating dummy data for demonstration...")
        
        # Create dummy data if Excel file is not available
        data.NoN = 244  # Assuming 244 nodes based on boundary conditions
        data.NoE = 942  # 942 elements
        
        # Dummy node coordinates (you would replace this with actual data)
        data.Node = np.random.rand(data.NoN, 3) * 100  # Random coordinates in inches
        
        # Dummy element connectivity
        data.Ele = np.random.randint(1, data.NoN+1, (data.NoE, 3))
        
        # Dummy material properties
        material_props = np.array([data.E, A, I, data.ro])
        data.Mat = np.kron(material_props, np.ones((data.nvars, 1)))
        
        # Dummy loads
        data.Nodeload = np.zeros((data.NoN, 4))
        data.Nodeload[:, 0] = np.arange(1, data.NoN + 1)  # Node numbers
        
        print("Using dummy data. Please provide the actual Excel file for real analysis.")
    
    # Prescribed displacement (boundary conditions)
    # Nodes 233-244 are fixed in all directions (1-based indexing)
    bound_nodes = np.arange(233, 245).reshape(-1, 1)  # nodes 233-244
    bound_dofs = np.tile([1, 1, 1], (12, 1))          # constrain all 3 DOFs
    data.Bound = np.hstack([bound_nodes, bound_dofs])
    
    # Variable bounds
    data.XB = np.array([1, 200])
    data.XV = np.arange(1, 201)  # 1 to 200
    
    return data, {
        'ro': data.ro,
        'fy': data.fy,
        'E': data.E,
        'nvars': data.nvars,
        'NoE': data.NoE,
        'XV': data.XV,
        'XB': data.XB,
        'Node': data.Node,
        'Ele': data.Ele,
        'Mat': data.Mat,
        'Eload': [],
        'Bound': data.Bound,
        'Nodeload': data.Nodeload,
    }

# Example usage and utility functions
def print_truss_info(data):
    """Print basic information about the truss"""
    print(f"942-bar Truss Optimization Problem")
    print(f"================================")
    print(f"Number of variables: {data.nvars}")
    print(f"Number of nodes: {data.NoN}")
    print(f"Number of elements: {data.NoE}")
    print(f"Load case: {data.lcase}")
    print(f"Material properties:")
    print(f"  - Density: {data.ro} lb/in³")
    print(f"  - Elastic modulus: {data.E} ksi")
    print(f"  - Yield strength: {data.fy} ksi")
    print(f"  - Maximum displacement: {data.dm} in")
    print(f"Variable bounds: [{data.XB[0]}, {data.XB[1]}]")
    print(f"Node coordinate range:")
    print(f"  - X: [{np.min(data.Node[:, 0]):.2f}, {np.max(data.Node[:, 0]):.2f}] in")
    print(f"  - Y: [{np.min(data.Node[:, 1]):.2f}, {np.max(data.Node[:, 1]):.2f}] in")
    print(f"  - Z: [{np.min(data.Node[:, 2]):.2f}, {np.max(data.Node[:, 2]):.2f}] in")

# Main execution
if __name__ == "__main__":
    # Create truss data
    try:
        truss_data, _ = truss942data('26StoreyTruss.xls', lcase=4)
        print_truss_info(truss_data)
        
        # Example of accessing data
        print(f"\nFirst 5 nodes (coordinates in inches):")
        print(truss_data.Node[:5])
        
        print(f"\nFirst 5 elements (connectivity):")
        print(truss_data.Ele[:5])
        
        print(f"\nBoundary conditions:")
        print(truss_data.Bound)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Excel file '26StoreyTruss.xls' is available")
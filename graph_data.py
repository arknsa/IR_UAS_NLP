import networkx as nx
import pandas as pd

# Load data again for use in code creation
file_path = "data_obat_uas.xlsx"
data = pd.read_excel(file_path)

# Initialize a directed graph
G = nx.DiGraph()

# Populate the graph using the provided dataset
for _, row in data.iterrows():
    # Main node: Medication name
    medication_name = row['name']

    # Adding nodes and edges for each relationship from the dataset
    # Manufacturer
    if pd.notna(row['Manufaktur']):
        G.add_edge(medication_name, row['Manufaktur'], relation="dibuat oleh")

    # Side effects
    if pd.notna(row['Efek Samping']):
        side_effects = row['Efek Samping'].split(", ")
        for side_effect in side_effects:
            G.add_edge(medication_name, side_effect.strip(), relation="memiliki efek samping")

    # General indication
    if pd.notna(row['Indikasi Umum']):
        G.add_edge(medication_name, row['Indikasi Umum'], relation="mengobati")

    # Composition
    if pd.notna(row['Komposisi']):
        composition = row['Komposisi'].split(", ")
        for comp in composition:
            G.add_edge(medication_name, comp.strip(), relation="mengandung")

    # Contraindications
    if pd.notna(row['Kontra Indikasi']):
        contraindications = row['Kontra Indikasi'].split(", ")
        for contraindication in contraindications:
            G.add_edge(medication_name, contraindication.strip(), relation="tidak cocok untuk")

def get_graph():
    return G
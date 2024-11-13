import dash_app
from dash_app import dcc, html
import plotly.graph_objects as go
import networkx as nx

# Visualisasi menggunakan Plotly
app = dash_app.Dash(__name__)

# Contoh graf kecil untuk visualisasi
G = nx.DiGraph()
G.add_edge("Viagra", "Sakit Kepala", relation="memiliki efek samping")
G.add_edge("Viagra", "Pfizer", relation="dibuat oleh")

# Fungsi visualisasi
def visualize_graph(G):
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = 0, 0
        x1, y1 = 1, 1
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = 0, 0
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10
        ))
    return go.Figure(data=[edge_trace, node_trace])

# Layout Dash
app.layout = html.Div([
    html.H1("Knowledge Graph Viewer"),
    dcc.Graph(
        id="graph-visualization",
        figure=visualize_graph(G)
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

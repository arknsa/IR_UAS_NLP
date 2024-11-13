from flask import Flask, request, jsonify
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
from flask_cors import CORS
from graph_data import get_graph

# Initialize Flask app
flask_app = Flask(__name__)
CORS(flask_app)

# Initialize Knowledge Graph
file_path = "data_obat_uas.xlsx"
G = get_graph()

# Extract options for dropdowns
entity_options = [{"label": node, "value": node} for node in G.nodes()]
relation_options = [
    {"label": "memiliki efek samping", "value": "memiliki efek samping"},
    {"label": "dibuat oleh", "value": "dibuat oleh"},
    {"label": "mengobati", "value": "mengobati"},
    {"label": "mengandung", "value": "mengandung"},
]

# Flask API for querying the Knowledge Graph
@flask_app.route('/query', methods=['GET'])
def query_graph():
    entity = request.args.get('entity')
    relation = request.args.get('relation')
    if not entity or not relation:
        return jsonify({"error": "Entity and relation are required"}), 400

    if entity in G:
        results = [
            neighbor
            for neighbor in G.neighbors(entity)
            if G[entity][neighbor].get('relation') == relation
        ]
        return jsonify({"results": results})
    else:
        return jsonify({"error": f"Entity '{entity}' not found"}), 404

# Initialize Dash app
dash_app = dash.Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')

# Function to visualize the graph
def visualize_graph(G):
    edge_x = []
    edge_y = []
    edge_labels = []
    for edge in G.edges(data=True):
        edge_x.append(edge[0])
        edge_y.append(edge[1])
        edge_labels.append(edge[2].get('relation', ''))

    node_trace = go.Scatter(
        x=list(range(len(G.nodes))),
        y=[0] * len(G.nodes),
        mode='markers+text',
        text=list(G.nodes),
        marker=dict(size=10, color='blue'),
    )

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines+text',
        text=edge_labels,
        line=dict(color='gray', width=1),
    )

    fig = go.Figure(data=[node_trace, edge_trace])
    return fig

# Dash layout with dropdowns
dash_app.layout = html.Div([
    html.H1("Knowledge Graph Viewer"),
    dcc.Graph(
        id="graph-visualization",
        figure=visualize_graph(G)  # Function to draw the Knowledge Graph
    ),
    html.Div([
        html.Label("Select Entity:"),
        dcc.Dropdown(
            id="entity-dropdown",
            options=entity_options,
            placeholder="Select an entity",
        ),
        html.Label("Select Relation:"),
        dcc.Dropdown(
            id="relation-dropdown",
            options=relation_options,
            placeholder="Select a relation",
        ),
        html.Button("Query", id="query-button"),
    ]),
    html.Div(id="query-result")
])

# Dash callback to handle query and display results
@dash_app.callback(
    Output("query-result", "children"),  # Where the results will be displayed
    Input("query-button", "n_clicks"),  # Triggered when button is clicked
    Input("entity-dropdown", "value"),  # Get the value of the entity dropdown
    Input("relation-dropdown", "value")  # Get the value of the relation dropdown
)
def update_query_result(n_clicks, entity, relation):
    if n_clicks is None:
        return "Select an entity and relation, then click Query."
    
    if not entity or not relation:
        return "Both entity and relation are required."
    
    # Make a request to the Flask API
    url = f"http://127.0.0.1:5000/query?entity={entity}&relation={relation}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            return f"Results: {', '.join(data['results'])}"
        else:
            return f"No results found for entity '{entity}' and relation '{relation}'."
    else:
        return f"Error: {response.json().get('error', 'Something went wrong')}"

# Run Flask app
if __name__ == '__main__':
    flask_app.run(debug=True)

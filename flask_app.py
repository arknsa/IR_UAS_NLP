from flask import Flask, request, jsonify
import networkx as nx

app = Flask(__name__)

# Simpan Knowledge Graph menggunakan NetworkX
G = nx.DiGraph()
# Tambahkan node dan edges pada graf...

@app.route('/query', methods=['GET'])
def query_graph():
    entity = request.args.get('entity')
    relation = request.args.get('relation')
    if not entity or not relation:
        return jsonify({"error": "Entity and relation are required"}), 400
    
    # Proses query graf
    if entity in G:
        results = [
            neighbor
            for neighbor in G.neighbors(entity)
            if G[entity][neighbor].get('relation') == relation
        ]
        return jsonify({"results": results})
    else:
        return jsonify({"error": f"Entity '{entity}' not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

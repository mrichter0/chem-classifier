from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism as iso


QUERY = "3_substructure"
# CONTROL = "1_nitrogens"


HERE = Path(__file__).resolve().parent
GRAPHS_DIR = HERE / "graphs"


def read_graph(path):
    rows = path.read_text(encoding="utf-8").splitlines()
    g = nx.Graph()
    mode = None
    title = ""

    for row in rows:
        row = row.strip()

        if row.startswith("title:"):
            title = row.split(":", 1)[1].strip()
            continue
        if row == "nodes:":
            mode = "nodes"
            continue
        if row == "edges:":
            mode = "edges"
            continue
        if not row or row.startswith("title:"):
            continue

        if mode == "nodes":
            left, right = row.split(" element=")
            g.add_node(int(left), element=right)

        if mode == "edges":
            left, right = row.split(" order=")
            a, b = left.split()
            g.add_edge(int(a), int(b), order=int(right))

    return g, title


def graph_base_name(path):
    suffix = ".graph.txt"
    name = path.name
    if name.endswith(suffix):
        return name[: -len(suffix)]
    return path.stem


def run_one(name):
    query_path = GRAPHS_DIR / f"{name}.graph.txt"
    query_graph, _ = read_graph(query_path)

    node_match = iso.categorical_node_match("element", None)
    edge_match = iso.categorical_edge_match("order", None)

    matches = []
    for target_path in sorted(GRAPHS_DIR.glob("*.graph.txt")):
        target_graph, target_title = read_graph(target_path)
        matcher = iso.GraphMatcher(
            target_graph,
            query_graph,
            node_match=node_match,
            edge_match=edge_match,
        )
        if matcher.is_isomorphic():
            matches.append(graph_base_name(target_path))

    match_text = ", ".join(matches) if matches else "<none>"
    print(f"QUERY = {name}; Matches = {match_text}")


def main():
    run_one(QUERY)
    if "CONTROL" in globals():
        run_one(CONTROL)


if __name__ == "__main__":
    main()

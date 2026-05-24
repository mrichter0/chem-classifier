from pathlib import Path
import networkx as nx
from networkx.algorithms import isomorphism as iso


QUERY = "2"
# CONTROL = "1_nitrogens"


HERE = Path(__file__).resolve().parent
GRAPHS_DIR = HERE / "graphs"


def read_graph(path):
    rows = path.read_text(encoding="utf-8").splitlines()
    g = nx.Graph()
    mode = None

    for row in rows:
        row = row.strip()

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

    return g


def graph_base_name(path):
    suffix = ".graph.txt"
    name = path.name
    if name.endswith(suffix):
        return name[: -len(suffix)]
    return path.stem


def collect_matches(name):
    query_path = GRAPHS_DIR / f"{name}.graph.txt"
    query_graph = read_graph(query_path)

    node_match = iso.categorical_node_match("element", None)
    edge_match = iso.categorical_edge_match("order", None)

    methods = [
        ("is_isomorphic()", "is_isomorphic"),
        ("subgraph_is_isomorphic()", "subgraph_is_isomorphic"),
        ("subgraph_is_monomorphic()", "subgraph_is_monomorphic"),
    ]

    results = []
    for label, method_name in methods:
        hits = []
        for target_path in sorted(GRAPHS_DIR.glob("*.graph.txt")):
            target_graph = read_graph(target_path)
            matcher = iso.GraphMatcher(
                target_graph,
                query_graph,
                node_match=node_match,
                edge_match=edge_match,
            )
            if getattr(matcher, method_name)():
                hits.append(graph_base_name(target_path))
        results.append((label, hits))

    return results


def print_summary(name):
    results = collect_matches(name)
    counts = " / ".join(str(len(hits)) for _, hits in results)
    details = "; ".join(
        f"{label} = {', '.join(hits) if hits else '<none>'}"
        for label, hits in results
    )
    print(f"QUERY = {name}; Matches = {counts}")
    print(details)
    print()


def main():
    print_summary(QUERY)
    if "CONTROL" in globals():
        print_summary(CONTROL)


if __name__ == "__main__":
    main()

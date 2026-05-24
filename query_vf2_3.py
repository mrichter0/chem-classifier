from pathlib import Path
import re
import networkx as nx
from networkx.algorithms import isomorphism as iso


QUERY = "1"
# CONTROL = "1_nitrogens"


HERE = Path(__file__).resolve().parent
GRAPHS_DIR = HERE / "graphs"


def parse_graph_block(block):
    rows = block.splitlines()
    g = nx.Graph()
    mode = None
    index = None

    for row in rows:
        row = row.strip()

        if row.startswith("index:"):
            index = int(row.split(":", 1)[1].strip())
            continue
        if row == "nodes:":
            mode = "nodes"
            continue
        if row == "edges:":
            mode = "edges"
            continue
        if not row:
            continue

        if mode == "nodes":
            left, right = row.split(" element=")
            g.add_node(int(left), element=right)

        if mode == "edges":
            left, right = row.split(" order=")
            a, b = left.split()
            g.add_edge(int(a), int(b), order=int(right))

    return index, g


def load_graph_file(path):
    text = path.read_text(encoding="utf-8")
    index, graph = parse_graph_block(text)
    return index, graph


def load_graphs_file(path):
    text = path.read_text(encoding="utf-8")
    records = []
    for block in text.split("\n---\n"):
        block = block.strip()
        if not block:
            continue
        index, graph = parse_graph_block(block)
        records.append((index, graph))
    return records


def parse_query_name(name):
    match = re.match(r"^(.*)\[(\d+)\]$", name)
    if match:
        return match.group(1), int(match.group(2))

    match = re.match(r"^(.*):(\d+)$", name)
    if match:
        return match.group(1), int(match.group(2))

    return name, None


def load_query(name):
    base, index = parse_query_name(name)

    single_path = GRAPHS_DIR / f"{base}.graph.txt"
    multi_path = GRAPHS_DIR / f"{base}.graphs.txt"

    if index is None and single_path.exists():
        _, graph = load_graph_file(single_path)
        return graph

    if multi_path.exists():
        for item_index, graph in load_graphs_file(multi_path):
            if item_index == index:
                return graph

    raise FileNotFoundError(f"Could not resolve query '{name}'")


def scan_targets():
    for path in sorted(GRAPHS_DIR.glob("*.graph.txt")):
        _, graph = load_graph_file(path)
        yield path.stem[:-6] if path.stem.endswith(".graph") else path.stem, graph

    for path in sorted(GRAPHS_DIR.glob("*.graphs.txt")):
        base = path.name[: -len(".graphs.txt")]
        for index, graph in load_graphs_file(path):
            yield f"{base}[{index}]", graph


def collect_matches(name):
    query_graph = load_query(name)

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
        for target_name, target_graph in scan_targets():
            matcher = iso.GraphMatcher(
                target_graph,
                query_graph,
                node_match=node_match,
                edge_match=edge_match,
            )
            if getattr(matcher, method_name)():
                hits.append(target_name)
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

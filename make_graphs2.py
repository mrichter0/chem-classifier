from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import networkx as nx


HERE = Path(__file__).resolve().parent
GRAPHS_DIR = HERE / "graphs"


@dataclass
class SDRecord:
    graph: nx.Graph


def split_lines(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def parse_v2000(lines: list[str]) -> nx.Graph:
    counts = lines[3].split()
    atom_count = int(counts[0])
    bond_count = int(counts[1])

    g = nx.Graph()
    atom_lines = lines[4 : 4 + atom_count]
    bond_lines = lines[4 + atom_count : 4 + atom_count + bond_count]

    for idx, row in enumerate(atom_lines, start=1):
        parts = row.split()
        g.add_node(idx, element=parts[3])

    for row in bond_lines:
        parts = row.split()
        a = int(parts[0])
        b = int(parts[1])
        order = int(parts[2])
        g.add_edge(a, b, order=order)

    return g


def parse_v3000(lines: list[str]) -> nx.Graph:
    g = nx.Graph()
    in_atoms = False
    in_bonds = False

    for row in lines:
        row = row.strip()

        if row == "M  V30 BEGIN ATOM":
            in_atoms = True
            continue
        if row == "M  V30 END ATOM":
            in_atoms = False
            continue
        if row == "M  V30 BEGIN BOND":
            in_bonds = True
            continue
        if row == "M  V30 END BOND":
            in_bonds = False
            continue

        if in_atoms:
            parts = row.split()
            atom_id = int(parts[2])
            element = parts[3]
            g.add_node(atom_id, element=element)

        if in_bonds:
            parts = row.split()
            order = int(parts[3])
            a = int(parts[4])
            b = int(parts[5])
            g.add_edge(a, b, order=order)

    return g


def mol_block_to_graph(text: str) -> nx.Graph:
    lines = split_lines(text)
    head = "\n".join(lines[:8])
    if "V3000" in head:
        return parse_v3000(lines)
    return parse_v2000(lines)


def read_sd(path: Path) -> list[SDRecord]:
    text = path.read_text(encoding="utf-8", errors="replace")
    records: list[SDRecord] = []

    for chunk in text.split("$$$$"):
        block = chunk.strip()
        if not block:
            continue

        lines = split_lines(block)
        end = lines.index("M  END")
        mol_block = "\n".join(lines[: end + 1])
        records.append(SDRecord(graph=mol_block_to_graph(mol_block)))

    return records


def graph_block(index: int, graph: nx.Graph) -> str:
    lines = [f"index: {index}", "nodes:"]
    for node_id, data in sorted(graph.nodes(data=True)):
        lines.append(f"  {node_id} element={data['element']}")
    lines.append("edges:")
    for a, b, data in sorted(graph.edges(data=True)):
        lines.append(f"  {a} {b} order={data['order']}")
    return "\n".join(lines)


def write_single_graph(path: Path, graph: nx.Graph) -> None:
    path.write_text(graph_block(0, graph) + "\n", encoding="utf-8")


def write_multi_graph(path: Path, records: list[SDRecord]) -> None:
    blocks = [graph_block(index, record.graph) for index, record in enumerate(records)]
    path.write_text("\n---\n".join(blocks) + "\n", encoding="utf-8")


def main() -> None:
    GRAPHS_DIR.mkdir(exist_ok=True)

    created: list[Path] = []

    for mol_path in sorted(HERE.glob("*.mol")):
        graph = mol_block_to_graph(mol_path.read_text(encoding="utf-8", errors="replace"))
        out_path = GRAPHS_DIR / f"{mol_path.stem}.graph.txt"
        write_single_graph(out_path, graph)
        created.append(out_path)

    for sd_path in sorted([*HERE.glob("*.sd"), *HERE.glob("*.sdf")]):
        records = read_sd(sd_path)
        out_path = GRAPHS_DIR / f"{sd_path.stem}.graphs.txt"
        write_multi_graph(out_path, records)
        created.append(out_path)

    for path in created:
        print(path.name)


if __name__ == "__main__":
    main()

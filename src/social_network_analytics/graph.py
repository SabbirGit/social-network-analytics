"""An undirected, unweighted network of people or organizations."""

import csv
from pathlib import Path


class SocialNetwork:
    """Store a simple graph with string node IDs and no self-loops."""

    def __init__(self):
        self._neighbors = {}
        self._edge_count = 0

    def add_node(self, node):
        """Add a node, including one with no relationships."""
        if not isinstance(node, str) or not node.strip():
            raise ValueError("Node IDs must be nonblank strings.")
        self._neighbors.setdefault(node, set())

    def add_edge(self, source, target):
        """Add a relationship. Repeated and reversed edges count once."""
        if source == target:
            raise ValueError("Self-loops are not supported.")
        for node in (source, target):
            if not isinstance(node, str) or not node.strip():
                raise ValueError("Node IDs must be nonblank strings.")
        self.add_node(source)
        self.add_node(target)
        if target not in self._neighbors[source]:
            self._neighbors[source].add(target)
            self._neighbors[target].add(source)
            self._edge_count += 1

    @classmethod
    def from_csv(cls, path):
        """Load edges from a UTF-8 CSV with source and target columns."""
        graph = cls()
        with Path(path).open(encoding="utf-8-sig", newline="") as stream:
            rows = csv.DictReader(stream, strict=True)
            if rows.fieldnames is None or any(
                rows.fieldnames.count(column) != 1 for column in ("source", "target")
            ):
                raise ValueError("CSV must contain one source and one target column.")
            for row in rows:
                try:
                    graph.add_edge((row["source"] or "").strip(), (row["target"] or "").strip())
                except ValueError as error:
                    raise ValueError(f"CSV line {rows.line_num}: {error}") from error
        return graph

    def degrees(self):
        """Return the number of neighbors for each node."""
        return {node: len(neighbors) for node, neighbors in self._neighbors.items()}

    def degree_centrality(self):
        """Return each degree divided by the maximum possible degree."""
        denominator = max(len(self._neighbors) - 1, 1)
        return {node: degree / denominator for node, degree in self.degrees().items()}

    def connected_components(self):
        """Return components sorted by size, with alphabetical tie-breaking."""
        seen = set()
        components = []
        for start in self._neighbors:
            if start in seen:
                continue
            seen.add(start)
            pending = [start]
            component = []
            while pending:
                node = pending.pop()
                component.append(node)
                unseen = self._neighbors[node] - seen
                seen.update(unseen)
                pending.extend(unseen)
            components.append(sorted(component))
        return sorted(components, key=lambda group: (-len(group), group))

    def clustering_coefficients(self):
        """Return the fraction of connected neighbor pairs for each node."""
        coefficients = {}
        for node, neighbors in self._neighbors.items():
            possible_twice = len(neighbors) * (len(neighbors) - 1)
            if possible_twice == 0:
                coefficients[node] = 0.0
                continue
            linked_twice = sum(len(neighbors & self._neighbors[other]) for other in neighbors)
            coefficients[node] = linked_twice / possible_twice
        return coefficients

    def summary(self):
        """Return network size, density, connectedness, and average clustering."""
        count = len(self._neighbors)
        possible_edges = count * (count - 1) // 2
        components = self.connected_components()
        return {
            "nodes": count,
            "edges": self._edge_count,
            "density": self._edge_count / possible_edges if possible_edges else 0.0,
            "components": len(components),
            "largest_component": len(components[0]) if components else 0,
            "average_clustering": sum(self.clustering_coefficients().values()) / count
            if count else 0.0,
        }

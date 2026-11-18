# Social Network Analytics

Analyze who is connected, who has the most connections, and how tightly people cluster. The package supports simple, undirected, unweighted networks and uses only the Python standard library at runtime.

## Install

From this directory, with Python 3.9 or later:

```powershell
python -m pip install .
```

## Analyze an edge list

Save this example as `relationships.csv`:

```csv
source,target
Ada,Lin
Lin,Grace
Grace,Ada
Grace,Sam
```

```powershell
social-network relationships.csv --nodes
```

The example has four nodes, four edges, one connected component, and density of about 0.67. Grace has the highest degree at three. Use `--nodes` to include degrees, degree centrality, local clustering coefficients, and component membership in the JSON output.

## Use from Python

```python
from social_network_analytics import SocialNetwork

network = SocialNetwork.from_csv("relationships.csv")
network.add_node("Taylor")  # Include an isolated person.
print(network.summary())
print(network.connected_components())
```

You can also start with `SocialNetwork()` and call `add_edge(source, target)`. Duplicate rows, including reversed pairs, count as one edge. Self-loops and blank IDs raise an error. CSV loading trims surrounding whitespace and ignores extra columns. Use the Python API to add isolated nodes because an edge list contains only endpoints.

Density is the fraction of all possible edges present. Degree centrality is degree divided by the number of other nodes. Local clustering is the fraction of a node’s neighbor pairs that are connected. Nodes with fewer than two neighbors have a clustering coefficient of zero and count toward the network average.

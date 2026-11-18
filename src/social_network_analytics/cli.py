"""Command-line interface for CSV network analysis."""

import argparse
import csv
import json

from .graph import SocialNetwork


def main():
    parser = argparse.ArgumentParser(description="Analyze an undirected CSV edge list.")
    parser.add_argument("csv_file", help="UTF-8 CSV with source and target columns")
    parser.add_argument("--nodes", action="store_true", help="include node-level metrics")
    args = parser.parse_args()
    try:
        graph = SocialNetwork.from_csv(args.csv_file)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))

    result = {"summary": graph.summary()}
    if args.nodes:
        result["degrees"] = graph.degrees()
        result["degree_centrality"] = graph.degree_centrality()
        result["clustering"] = graph.clustering_coefficients()
        result["connected_components"] = graph.connected_components()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

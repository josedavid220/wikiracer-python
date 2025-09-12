# Wikiracer (Python)

Python implementation to solve the Wikiracer game.

## Overview

This repository provides:
- A simple HTML parser to extract Wikipedia-style links.
- A Dijkstra-based search implementation to find shortest-cost paths.
- A heuristic variant that prioritizes links closer to the goal by string similarity using the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

## Setup

Clone the repository:
```bash
git clone https://github.com/josedavid220/wikiracer-python.git
```

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). Then run this command to install dependencies and the appropiate python version:
```bash
uv sync
```

## Testing

From the repository root:

```python
  uv run pytest
```

## Summary of current results

The included [results](./results/results.txt) contains pairwise runs between a small set of pages. High-level stats:

- Number of measured pairs: 15
- Total recorded requests across all runs: 62
- Average requests per pair: 4.13
- Minimum requests observed: 1  (e.g. ('Michael_Jordan','Kobe_Bryant') and ('United_Nations','Brazil'))
- Maximum requests observed: 9  (e.g. ('Jesus','Michael_Jordan') and ('Kobe_Bryant','Brazil'))
- Observed path lengths range from 2 up to 6.

All tests were passed in 56.56s.
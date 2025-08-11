# Open SWE Demo

This repository provides a tiny, dependency free reimplementation of the
concepts demonstrated in the [`open-swe`][open-swe] project.  It offers a Python
API for creating agents, registering tools and wiring them together in a workflow
graph.

## Example

```python
from open_swe.app import create_app

graph = create_app()
outputs = graph.run("planner", "build a web app")
print(outputs)
```

The above script constructs a graph with a planning agent feeding into a coding
agent and runs a simple prompt through the graph.

[open-swe]: https://github.com/langchain-ai/open-swe/tree/main/apps/open-swe

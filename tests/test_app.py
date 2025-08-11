from open_swe.app import create_app


def test_graph_execution():
    graph = create_app()
    outputs = graph.run("planner", "write docs")
    assert outputs[0][0] == "planner"
    assert outputs[1][0] == "coder"
    assert len(outputs) == 2

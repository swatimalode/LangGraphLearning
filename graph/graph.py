from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode

from tool_registry import tool_registry
from graph.state import GraphState
from graph.nodes import call_llm
from graph.edges import should_continue


def create_graph():

    graph = StateGraph(GraphState)

    tool_node = ToolNode(tool_registry)

    graph.add_node("llm", call_llm)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "llm")

    graph.add_conditional_edges(
        "llm",
        should_continue
    )

    graph.add_edge("tools", "llm")

    return graph.compile()


CompiledStateGraph = create_graph()
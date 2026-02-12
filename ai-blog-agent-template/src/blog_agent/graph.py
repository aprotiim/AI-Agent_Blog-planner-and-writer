from __future__ import annotations

from datetime import date
from typing import Dict

from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from .schemas import State
from .nodes.router import route_node, route_next
from .nodes.research import research_node
from .nodes.orchestrator import orchestrator_node
from .nodes.worker import worker_node
from .nodes.reducer import merge_node, decide_images_node, generate_and_place_images_node


def fanout(state: State):
    assert state["plan"] is not None
    return [
        Send(
            "worker",
            {
                "task": task.model_dump(),
                "topic": state["topic"],
                "mode": state["mode"],
                "as_of": state["as_of"],
                "recency_days": state["recency_days"],
                "plan": state["plan"].model_dump(),
                "evidence": [e.model_dump() for e in state.get("evidence", [])],
            },
        )
        for task in state["plan"].tasks
    ]



#def _worker_adapter(inputs: Dict) -> Dict:
    # inputs contains {"task": Task, "state": State}
    #return worker_node(inputs["task"], inputs["state"])


reducer_graph = StateGraph(State)
reducer_graph.add_node("merge_content", merge_node)
reducer_graph.add_node("decide_images", decide_images_node)
reducer_graph.add_node("generate_and_place_images", generate_and_place_images_node)
reducer_graph.add_edge(START, "merge_content")
reducer_graph.add_edge("merge_content", "decide_images")
reducer_graph.add_edge("decide_images", "generate_and_place_images")
reducer_graph.add_edge("generate_and_place_images", END)
reducer_subgraph = reducer_graph.compile()

# -----------------------------
# 9) Build main graph
# -----------------------------
g = StateGraph(State)
g.add_node("router", route_node)
g.add_node("research", research_node)
g.add_node("orchestrator", orchestrator_node)
g.add_node("worker", worker_node)
g.add_node("reducer", reducer_subgraph)

g.add_edge(START, "router")
g.add_conditional_edges("router", route_next, {"research": "research", "orchestrator": "orchestrator"})
g.add_edge("research", "orchestrator")

g.add_conditional_edges("orchestrator", fanout, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()
app



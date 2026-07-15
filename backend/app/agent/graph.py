from typing import TypedDict, Annotated, Sequence, Dict, Any, List, Optional
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, add_messages
from .llm import get_llm
from .tools import get_hcp_profile, log_interaction, edit_interaction, analyze_compliance, generate_follow_up
import json

# Define the State of our Agentic Graph
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    hcp_id: Optional[int]
    extracted_state: Optional[Dict[str, Any]]
    compliance_check: Optional[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, Any]]]

# Map tool names to tool instances
tools_map = {
    "get_hcp_profile": get_hcp_profile,
    "log_interaction": log_interaction,
    "edit_interaction": edit_interaction,
    "analyze_compliance": analyze_compliance,
    "generate_follow_up": generate_follow_up
}

# Define the nodes
def call_model(state: AgentState):
    messages = state["messages"]
    llm = get_llm()
    
    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(list(tools_map.values()))
    
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def execute_tools(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return {}
        
    tool_responses = []
    extracted_state = state.get("extracted_state") or {}
    compliance_check = state.get("compliance_check") or {}
    recommendations = state.get("recommendations") or []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]
        
        # Execute tool
        tool_instance = tools_map.get(tool_name)
        if tool_instance:
            try:
                result_str = tool_instance.invoke(tool_args)
                tool_responses.append(
                    ToolMessage(content=result_str, tool_call_id=tool_id, name=tool_name)
                )
                
                # Parse result and update UI states
                try:
                    result_data = json.loads(result_str)
                    if tool_name == "log_interaction":
                        # Log interaction fills the extracted state
                        extracted_state = {
                            "hcp_id": tool_args.get("hcp_id"),
                            "date": tool_args.get("date"),
                            "channel": tool_args.get("channel"),
                            "transcript": tool_args.get("transcript"),
                            "summary": tool_args.get("summary"),
                            "discussion_topics": tool_args.get("discussion_topics"),
                            "follow_up_date": tool_args.get("follow_up_date"),
                            "compliance_status": result_data.get("compliance_status"),
                            "compliance_notes": result_data.get("compliance_notes"),
                            "sentiment": tool_args.get("sentiment"),
                            "next_steps": tool_args.get("next_steps"),
                            "logged_id": result_data.get("interaction_id")
                        }
                    elif tool_name == "analyze_compliance":
                        compliance_check = result_data
                    elif tool_name == "generate_follow_up":
                        recommendations.append(result_data)
                    elif tool_name == "get_hcp_profile":
                        # If we fetch HCP profile, update current HCP ID in state
                        pass
                except Exception:
                    # Not JSON, keep as is
                    pass
            except Exception as e:
                tool_responses.append(
                    ToolMessage(content=f"Error executing tool {tool_name}: {str(e)}", tool_call_id=tool_id, name=tool_name)
                )
        else:
            tool_responses.append(
                ToolMessage(content=f"Tool {tool_name} not found.", tool_call_id=tool_id, name=tool_name)
            )
            
    return {
        "messages": tool_responses,
        "extracted_state": extracted_state,
        "compliance_check": compliance_check,
        "recommendations": recommendations
    }

# Define the routing logic
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM made a tool call, route to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "continue"
    return "end"

# Build the graph workflow
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", call_model)
workflow.add_node("action", execute_tools)

# Set entry point
workflow.set_entry_point("agent")

# Add conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": "__end__"
    }
)

# Add edge from action back to agent
workflow.add_edge("action", "agent")

# Compile graph
app_graph = workflow.compile()

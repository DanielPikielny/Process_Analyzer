import streamlit as st
from analyzer import extract_steps, find_inefficiencies, suggest_automations, suggest_tools, estimate_costs
from schema import validate_output
from diagram import create_workflow_diagram

IMPACT_COLOUR = {"low": "🟢", "medium": "🟡", "high": "🔴"}

st.title("AI Process Analyzer")

workflow = st.text_area(
    "Describe a business workflow",
    height=200
)

if st.button("Analyze Process"):

    if not workflow.strip():
        st.warning("Please describe a workflow before analyzing.")
    else:
        with st.spinner("Step 1/5 — Extracting process steps..."):
            steps = extract_steps(workflow)

        if steps is None:
            st.error("Failed to extract process steps.")
            st.stop()

        st.subheader("Process Steps")
        for item in steps:
            with st.expander(f"• {item.description}  —  confidence {item.confidence:.0%}"):
                st.write(item.explanation)

        st.subheader("Workflow Diagram")
        diagram = create_workflow_diagram([s.description for s in steps])
        st.graphviz_chart(diagram.source)

        with st.spinner("Step 2/5 — Identifying inefficiencies..."):
            inefficiencies = find_inefficiencies(steps)

        if inefficiencies is None:
            st.error("Failed to identify inefficiencies.")
            st.stop()

        st.subheader("Inefficiencies")
        for item in inefficiencies:
            icon = IMPACT_COLOUR.get(item.impact, "•")
            with st.expander(f"{icon} {item.description}  —  {item.impact} impact  —  confidence {item.confidence:.0%}"):
                st.write(item.explanation)

        with st.spinner("Step 3/5 — Suggesting automations..."):
            automations = suggest_automations(steps, inefficiencies)

        if automations is None:
            st.error("Failed to suggest automations.")
            st.stop()

        st.subheader("Automation Opportunities")
        for item in automations:
            with st.expander(f"• {item.description}  —  confidence {item.confidence:.0%}"):
                st.write(item.explanation)

        with st.spinner("Step 4/5 — Recommending tools..."):
            tools = suggest_tools(automations)

        if tools is None:
            st.error("Failed to suggest tools.")
            st.stop()

        st.subheader("Suggested Tools")
        for item in tools:
            with st.expander(f"• {item.name}  —  confidence {item.confidence:.0%}"):
                st.write(item.explanation)

        with st.spinner("Step 5/5 — Estimating costs..."):
            costs = estimate_costs(automations, tools)

        if costs is None:
            st.error("Failed to estimate costs.")
            st.stop()

        st.subheader("Cost Estimates")
        for item in costs:
            with st.expander(f"• {item.item}  —  {item.estimate}"):
                st.write(item.notes)

        result = {
            "process_steps": steps,
            "inefficiencies": inefficiencies,
            "automation_opportunities": automations,
            "suggested_tools": tools,
            "cost_estimates": costs,
        }

        if not validate_output(result):
            st.warning("Analysis completed but some fields may be incomplete.")

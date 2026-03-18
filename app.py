import streamlit as st
from analyzer import analyze_process
from diagram import create_workflow_diagram

st.title("AI Process Analyzer")

workflow = st.text_area(
    "Describe a business workflow",
    height=200
)

if st.button("Analyze Process"):

    if not workflow.strip():
        st.warning("Please describe a workflow before analyzing.")
    else:
        with st.spinner("Analyzing workflow..."):
            result = analyze_process(workflow)

        if "error" in result:
            st.error(result["error"])

        else:
            st.subheader("Process Steps")
            for step in result["process_steps"]:
                st.write("•", step)

            st.subheader("Workflow Diagram")
            diagram = create_workflow_diagram(result["process_steps"])
            st.graphviz_chart(diagram.source)

            st.subheader("Inefficiencies")
            for item in result["inefficiencies"]:
                st.write("•", item)

            st.subheader("Automation Opportunities")
            for item in result["automation_opportunities"]:
                st.write("•", item)

            st.subheader("Suggested Tools")
            for tool in result["suggested_tools"]:
                st.write("•", tool)
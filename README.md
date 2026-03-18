# AI Process Analyzer

This project is a Streamlit-based web application designed to analyze business workflow descriptions. It uses Large Language Models to identify sequential process steps, pinpoint inefficiencies, and suggest automation opportunities and relevant software tools.

Features

    Workflow Extraction: Converts unstructured text descriptions into clear, sequential process steps.

    Visual Mapping: Automatically generates a flowchart diagram of the described workflow using Graphviz.

    Inefficiency Identification: Highlights manual bottlenecks and risks within the current process.

    Automation Recommendations: Provides concrete actions to improve efficiency through automation.

    Tool Suggestions: Recommends specific platforms or APIs to implement the suggested improvements.

Technical Architecture

    app.py: The frontend interface built with Streamlit, handling user input and displaying the structured analysis.

    analyzer.py: The core logic that interfaces with the OpenAI API to process text using the gpt-4o-mini model.

    diagram.py: A utility script that uses the Graphviz library to programmatically create workflow nodes and edges.

    schema.py: Ensures data integrity by validating that the model output contains all required JSON fields.

    process_prompt.txt: A system prompt template that enforces a strict JSON output format for consistent parsing.

Directory Structure:
    Ensure the prompt template is located in a prompts/ directory relative to the execution folder:
    ├── app.py
    ├── analyzer.py
    ├── diagram.py
    ├── schema.py
    └── prompts/
        └── process_prompt.txt

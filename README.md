# AI Process Analyzer

A Python-based analysis pipeline that transforms unstructured business workflow descriptions into structured insights. This tool identifies sequential steps, detects inefficiencies, suggests automation opportunities, recommends specific software tools, and provides rough cost estimates.
 Features

    Structured Analysis Pipeline: Uses a multi-step LLM chain to ensure high-quality, specialized analysis for each phase of the process.

    Automatic Visualization: Generates a workflow diagram using Graphviz to map out the current process steps.

    Confidence Scoring: Every insight includes a confidence score (0.0–1.0), giving users transparency into the AI's certainty.

    Modern Web UI: Built with Streamlit for an interactive, easy-to-use experience.

    Pydantic Validation: All data is strictly validated against a schema to ensure consistent output quality.

 Architecture

The project is divided into specialized modules:

    app.py: The Streamlit frontend and UI logic.

    analyzer.py: The core engine that manages LLM calls and the analysis sequence.

    schema.py: Pydantic models defining the data structure for every step of the pipeline.

    diagram.py: Logic for generating visual process maps.

 Prerequisites

    Python 3.9+

    An OpenAI API Key

    Graphviz installed on your system (required for the diagramming feature)

Data Schema

    The analyzer provides structured data in the following categories:
    
    | Component | Description |
    
    | :--- | :--- |
    
    | Process Steps | Sequential actions making up the workflow. |
    
    | Inefficiencies | High/Medium/Low impact bottlenecks and manual risks. |
    
    | Automations | Concrete opportunities for technical optimization. |
    
    | Suggested Tools | Specific software platforms (e.g., Zapier, HubSpot). |
    
    | Cost Estimates | Implementation effort or subscription pricing. |

Directory Structure:
    Ensure the prompt template is located in a prompts/ directory relative to the execution folder:
    ├── app.py
    
    ├── analyzer.py
    
    ├── diagram.py
    
    ├── schema.py
    
    └── prompts/
    
        └── process_prompt.txt

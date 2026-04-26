# IAFIT
#IMPORTANTE: CORRER EN EL PUERTO 8001
pip install -r requirements.txt
para instalar las dependencias

.\venv\Scripts\python.exe -m pip install -r requirements.txt
para ejecutar el servidor e instalar dependencias

# IAFIT - Intelligent Campus Assistant

IAFIT is an intelligent assistant system based on Retrieval-Augmented Generation (RAG) designed for the EAFIT University community. The system facilitates access to institutional information by allowing users to resolve queries in natural language, grounding all responses in official university documents to ensure technical accuracy and prevent hallucinations.

## Core Features

The system is structured into specific modules to handle different types of university data:

* Academic Queries: Processes regulations, calendar dates, and administrative protocols.
* Assisted Navigation: Provides text-based guidance for blocks, auditoriums, and cafeterias.
* Smart Directory: Locates professor offices and contact information.
* Events and Agenda: Manages information regarding cultural and academic campus activities.

## Technical Design and Testing

The project incorporates a rigorous acceptance and usability test design to ensure the reliability of the RAG pipeline.

### Brand Identity
The interface follows a specific visual framework to maintain institutional alignment:
* Purpose: Helpful and academic communication.
* Visuals: Standardized logo, color palette, and typography.
* Reference: [IAFIT: Brand Identity](https://canva.link/xrsi1glswcgshl9)

### Validation
Acceptance tests verify the system's ability to retrieve context and generate grounded answers. Functional demonstrations of the AI integration can be found in the project documentation videos.

## Installation and Setup

Follow these steps to configure the environment and run the assistant locally.

### 1. Environment Preparation
It is recommended to use a virtual environment to isolate dependencies and avoid version conflicts with other Python projects.

Command:
python -m venv venv

Activation (Windows):
.\venv\Scripts\activate

Activation (Linux/macOS):
source venv/bin/activate

### 2. Dependency Installation
Install the required libraries listed in the requirements file. This includes the LLM orchestration framework and vector database drivers.

Command:
pip install -r requirements.txt

### 3. Configuration
The system requires environment variables to access the LLM provider and the vector store. Create a .env file in the root directory.

Required variables:
* API_KEY
* DATABASE_URL: Connection string for the vector index.

## Running the Program

The assistant can be executed via the command line. The main script accepts parameters to define the execution mode.

### Basic Execution
To start the standard interactive assistant:
python main.py

### Commands and Parameters
The system supports the following flags for specific configurations:

* --mode [chat|index]: 
    * chat: Starts the interactive natural language interface (default).
    * index: Updates the local vector database with new documents from the data folder.
* --source [path]:
    * Specifies a custom directory for PDF or text documents to be processed during indexing.
* --temperature [0.0 - 1.0]:
    * Adjusts the creativity of the response. A lower value (e.g., 0.1) is used for technical accuracy in regulations.

Example for indexing new regulations:
python main.py --mode index --source ./documents/regulations

Example for running the assistant with high precision:
python main.py --mode chat --temperature 0.2

## Documentation Reference

For further technical details regarding the component architecture or deployment diagrams, refer to the project Wiki:
* [Specific Requirements](https://github.com/Diego-Alejandro-angarita/IAFIT/wiki/Specific-requirements)
* [Component Diagram](https://github.com/Diego-Alejandro-angarita/IAFIT/wiki/Component-Diagram:-IAFIT)
* [Acceptance Test Design](https://github.com/Diego-Alejandro-angarita/IAFIT/wiki/Acceptance-and-Usability-Test-Design)

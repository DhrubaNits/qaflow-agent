# QAFlow Agent

QAFlow Agent is an AI-powered human-in-the-loop QA workflow assistant built for QA teams.

It supports the complete QA lifecycle from product requirement intake to release readiness. QAFlow helps QA teams review requirements, identify missing details, generate test scenarios, write test cases, perform peer review, analyze risk and coverage, capture execution results, triage failures, recommend fixes, generate release readiness summaries, and produce final QA reports.

The project uses **Gemini**, **Google ADK**, **Google Cloud Run**, **Google Agent Runtime**, **MongoDB MCP**, **MongoDB Atlas**, and **Google Secret Manager**.

QAFlow was built for the **MongoDB partner track**. MongoDB is not only used as storage. In this project, MongoDB Atlas and MongoDB MCP act as the persistent QA memory and RAG layer for the agent workflow.

---

## Required Technology Proof

QAFlow uses all required technologies at runtime:

| Requirement | Where it is used | Proof in code |
|---|---|---|
| Gemini | Powers QA agent reasoning for requirement analysis, test generation, triage, and release readiness | `qaflow/agent.py` |
| Google ADK / Agent Builder | Defines and runs the QAFlow agent workflow | `qaflow/agent.py` |
| Google Agent Runtime | Deploys the ADK agent as a managed agent runtime | `qaflow/agent_runtime_app.py`, `qaflow/agent_engine_entry.py` |
| MongoDB MCP | Connects the agent to MongoDB for saving and retrieving QA workflow artifacts | `mongodb-mcp-cloudrun/`, `MONGODB_MCP_URL` |
| MongoDB Atlas | Stores QA artifacts as persistent memory and RAG context | `qaflow.qa_analyses` collection |
| Google Cloud Run | Hosts the QAFlow web app, backend APIs, and MongoDB MCP service | Cloud Run deployment |
| Secret Manager | Stores MongoDB connection string securely | Cloud Run environment/secret config |

Runtime flow:

```text
QAFlow Web App on Cloud Run
    -> Gemini + Google ADK Agent
    -> Google Agent Runtime
    -> MongoDB MCP service on Cloud Run
    -> MongoDB Atlas qaflow.qa_analyses
```




## Demo

Hosted App URL:

```text
https://qaflow-agent-512657306508.us-central1.run.app
```

Demo Video:

```text
https://youtu.be/kWapgm7qwAY
```

---

## Problem Statement

In QA teams, actual test execution is only one part of the work. A large amount of time is spent on understanding requirements, identifying missing details, preparing test scenarios, writing test cases, reviewing coverage, checking risks, analyzing failures, and preparing release reports.

This information is often spread across requirement documents, chats, test cases, defect tickets, spreadsheets, automation reports, and release notes. Because of that, QA teams can lose context, miss risks, and repeat the same analysis again.

QAFlow solves this by providing an end-to-end AI-assisted QA workflow with persistent memory, traceability, and human approval gates.

---

## What QAFlow Does

QAFlow supports the QA workflow chronologically from product requirement to release decision.

1. **Requirement Intake**
   A Product Owner, Business Analyst, or QA user enters a requirement or user story.

2. **Save Requirement**
   QAFlow saves the original requirement into MongoDB as the first traceable QA artifact.

3. **Requirement Gap Analysis**
   QAFlow checks whether the requirement is clear enough for QA. It identifies missing details, unclear acceptance criteria, risks, edge cases, negative scenarios, test data needs, and clarifying questions.

4. **Requirement Approval Gate**
   A human reviewer can approve or reject the requirement. QAFlow does not continue blindly without human approval.

5. **Requirement Understanding**
   QAFlow extracts business intent, scope, impacted areas, assumptions, dependencies, and QA focus areas.

6. **Generate Test Scenarios**
   QAFlow creates positive, negative, boundary, regression, performance, and error-handling scenarios.

7. **Write Test Cases**
   QAFlow generates structured test cases with test steps, test data, expected results, priority, and coverage focus.

8. **Test Case Peer Review**
   QAFlow reviews generated test cases for missing coverage, weak cases, unclear expected results, and improvement areas.

9. **Test Case Approval Gate**
   A QA Lead can approve the test cases or provide rework notes before execution.

10. **Risk and Coverage Analysis**
    QAFlow identifies high-risk areas, coverage gaps, must-run tests, regression impact, and release risk.

11. **Test Execution Input**
    QAFlow supports simulated execution for demo purposes or manual execution input from QA/automation runs.

12. **Failure Triage**
    QAFlow analyzes failed outcomes and suggests probable root cause, severity, ownership direction, and triage summary.

13. **Fix Recommendation**
    QAFlow suggests corrective actions, validation focus, and next QA checks.

14. **Release Readiness**
    QAFlow summarizes test status, blockers, open risks, and final QA recommendation.

15. **Final QA Report and Release Approval**
    QAFlow generates a stakeholder-ready QA report and supports final human release approval. The report can be downloaded as a PDF.

---

## Key Features

* End-to-end QA workflow automation
* Requirement gap analysis
* Test scenario generation
* Structured test case generation
* Test case peer review
* Human-in-the-loop approval gates
* Risk and coverage analysis
* Execution result analysis
* Failure triage
* Fix recommendation
* Release readiness summary
* Final QA report generation
* PDF report download
* MongoDB-backed persistent QA memory
* MongoDB MCP-based RAG workflow
* Cloud Run-hosted web application
* Agent Runtime deployment

---

## MongoDB MCP and RAG Memory

MongoDB is a core part of QAFlow.

QAFlow uses MongoDB Atlas and MongoDB MCP as the persistent memory and RAG layer for the QA agent workflow.

All major QA artifacts are stored in MongoDB, including:

* Requirements
* Requirement gap analysis
* Requirement understanding
* Test scenarios
* Test cases
* Peer review notes
* Risk and coverage analysis
* Execution summaries
* Failure triage results
* Fix recommendations
* Release readiness summaries
* Final QA reports

These records are stored in the following collection:

```text
qaflow.qa_analyses
```

MongoDB MCP allows the agent to save and retrieve QA workflow records from MongoDB. This gives QAFlow memory across workflow steps.

For example:

* Test case generation can use requirement analysis as context.
* Peer review can use generated test cases as context.
* Release readiness can use risk analysis and execution results as context.
* Future requirements can reuse previous QA knowledge, gaps, and failure patterns.

In simple terms, MongoDB is not just a database in QAFlow. It is the persistent QA knowledge base that powers traceability, reuse, and RAG-based agent reasoning.

Final MongoDB-powered architecture:

```text
QAFlow Agent Runtime -> MongoDB MCP on Cloud Run -> MongoDB Atlas -> qaflow.qa_analyses
```

---

## Google Cloud and Agent Runtime Usage

QAFlow uses Google Cloud services to run the application and agent workflow.

### Google Cloud Run

Cloud Run hosts:

* QAFlow web application
* FastAPI backend
* API endpoints
* MongoDB MCP Cloud Run service

### Google Agent Runtime

The QAFlow ADK agent is deployed on Google Agent Runtime using the Vertex AI Agent Engine SDK.

Agent Runtime provides:

* Managed agent deployment
* Playground testing
* Sessions
* Traces
* Identity
* Security
* Monitoring support

### Google Secret Manager

Secret Manager stores sensitive configuration, such as the MongoDB connection string.

The MongoDB MCP service reads the MongoDB connection string securely from Secret Manager instead of hardcoding credentials.

### Gemini and Google ADK

QAFlow uses Gemini and Google ADK for agent reasoning and workflow orchestration.

Gemini powers the reasoning for requirement analysis, test design, risk coverage, failure triage, fix recommendation, and release readiness.

Google ADK is used to define and run the agent workflow.

---

## Architecture

High-level architecture:

```text
User / QA Team
    |
    v
QAFlow Web App on Cloud Run
    |
    v
FastAPI Backend
    |
    v
Gemini + Google ADK Agent
    |
    v
Google Agent Runtime
    |
    v
MongoDB MCP on Cloud Run
    |
    v
MongoDB Atlas - qaflow.qa_analyses
```

Human approval gates are included at critical stages:

```text
Requirement Approval -> Test Case Approval -> Release Approval
```

These gates ensure that AI supports QA teams but does not replace human judgment.

---

## Tech Stack

| Area                       | Technology                             |
| -------------------------- | -------------------------------------- |
| Agent Reasoning            | Gemini                                 |
| Agent Framework            | Google ADK                             |
| Managed Agent Deployment   | Google Agent Runtime                   |
| Web Hosting                | Google Cloud Run                       |
| Backend                    | FastAPI                                |
| Persistent Memory / RAG    | MongoDB Atlas                          |
| Tool Integration           | MongoDB MCP                            |
| Secrets                    | Google Secret Manager                  |
| Frontend                   | HTML, CSS, JavaScript                  |
| Package / Agent Deployment | agents-cli, Vertex AI Agent Engine SDK |
| Report Export              | PDF download                           |

---

## Project Structure

```text
qaflow-agent/
├── mongodb-mcp-cloudrun/        # MongoDB MCP Cloud Run service
├── qaflow/                      # Core agent code
│   ├── agent.py                 # Main ADK agent logic
│   ├── agent_runtime_app.py     # Agent Runtime application logic
│   └── app_utils/               # Utilities and helpers
├── tests/                       # Unit, integration, and load tests
├── GEMINI.md                    # AI-assisted development guide
├── SAFETY_GUARDRAILS.md         # Safety and governance documentation
├── AGENT_BUILDER_INTEGRATION.md # Agent Builder / integration details
├── pyproject.toml               # Project dependencies
├── Dockerfile                   # Cloud Run container setup
└── README.md                    # Project documentation
```

---

## Requirements

Before running the project, install:

* Python 3.11+
* uv
* Google Cloud SDK
* agents-cli
* Node.js, if running MongoDB MCP locally
* MongoDB Atlas connection string
* Google Cloud project with required APIs enabled

Install Agents CLI:

```bash
uvx google-agents-cli setup
```

Install project dependencies:

```bash
agents-cli install
```

---

## Environment Variables

Create environment variables for local development or configure them in Cloud Run / Agent Runtime.

```bash
QAFLOW_MODEL=gemini-2.5-flash
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<your-google-cloud-project-id>
GOOGLE_CLOUD_LOCATION=us-central1
MONGODB_CONNECTION_STRING=<your-mongodb-atlas-connection-string>
MONGODB_MCP_URL=<your-remote-mongodb-mcp-cloud-run-url>
```

Do not commit secrets to GitHub. Use Google Secret Manager for production deployments.

---

## Run Locally

Install dependencies:

```bash
agents-cli install
```

Run the local agent playground:

```bash
agents-cli playground
```

Run tests:

```bash
uv run pytest tests/unit tests/integration
```

Run the FastAPI app locally, if applicable:

```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 8080
```

---

## Deploy to Google Cloud Run

Set your Google Cloud project:

```bash
gcloud config set project <your-project-id>
```

Build and deploy the application to Cloud Run:

```bash
gcloud run deploy qaflow-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

Deploy MongoDB MCP as a separate Cloud Run service, then configure the app or Agent Runtime with:

```bash
MONGODB_MCP_URL=<mongodb-mcp-cloud-run-service-url>
```

---

## Deploy to Agent Runtime

Deploy the ADK agent to Google Agent Runtime:

```bash
agents-cli deploy
```

Or deploy using the configured Agent Runtime / Vertex AI Agent Engine SDK setup.

After deployment, verify the agent in Agent Runtime Playground.

The final tested flow is:

```text
Agent Runtime Playground -> QAFlow Agent -> MongoDB MCP Cloud Run Service -> MongoDB Atlas
```

---

## Safety and Human-in-the-Loop Governance

QAFlow includes human approval gates for critical QA decisions:

1. Requirement approval
2. Test case approval
3. Release approval

This ensures that AI-generated output is reviewed before the workflow continues.

QAFlow is designed to support QA teams, not replace human judgment. The agent helps reduce repetitive work, highlight risks, organize QA context, and improve traceability.

See:

```text
SAFETY_GUARDRAILS.md
```

---

## Accomplishments

* Built a working end-to-end QA workflow assistant
* Deployed the web app on Google Cloud Run
* Deployed the ADK agent on Google Agent Runtime
* Used MongoDB MCP as the RAG and memory layer
* Stored QA workflow artifacts in MongoDB Atlas
* Added human approval gates for realistic QA governance
* Generated final QA reports with PDF download
* Proved Agent Runtime to MongoDB read/write flow through MongoDB MCP

---

## What We Learned

We learned that building an agent is not only about prompts. A useful real-world agent needs tools, memory, deployment, security, observability, and human governance.

We also learned that MCP works best as a separate remote service for Agent Runtime deployments. Moving MongoDB MCP to Cloud Run made the architecture cleaner and allowed the Agent Runtime agent to connect to MongoDB reliably.

Most importantly, we learned that QA agents should not replace human judgment. They should reduce repetitive analysis, preserve context, highlight risks, and help QA teams make better release decisions.

---

## What's Next

Future improvements include:

* Azure DevOps, Jira, Zephyr, and TestRail integration
* Playwright, Selenium, UiPath, Postman, JMeter, and CI/CD execution result integration
* MongoDB-powered QA analytics dashboards
* Similar requirement search using MongoDB memory
* Historical defect and failure pattern retrieval
* Role-based approval workflow
* Better release risk prediction using stored QA history

---

## License

This project is licensed under the MIT License.

See:

```text
LICENSE
```

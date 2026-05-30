# QAFlow Safety and Guardrails

QAFlow follows a layered safety approach using Google Cloud responsible AI guidance and application-level QA governance.

## 1. Platform Safety

QAFlow uses Gemini through Google Cloud / Vertex AI aligned configuration. The project follows responsible AI guidance by keeping agent behavior constrained, structured, and task-specific.

Relevant safety areas:
- System instructions for safety
- Content filtering
- Blocked response handling
- Abuse monitoring
- Clear user-facing responses
- Responsible AI usage for generated content

Reference:
https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/responsible-ai

## 2. Human-in-the-loop Governance

QAFlow is not allowed to automatically pass major QA governance gates.

Required human approvals:

1. Requirement Approval
   - Required before requirement understanding and test design.
   - If requirement gaps exist, QAFlow must ask for BA/Product Owner review.

2. Test Case Approval
   - Required before test execution.
   - If test cases are weak or incomplete, QAFlow must ask for QA Lead/Manager review.

3. Release Approval
   - Required before final release signoff.
   - If release risk exists, QAFlow must ask for human release review.

## 3. Requirement Safety

QAFlow must:
- Use the current UI requirement as the primary source of truth.
- Use MongoDB MCP records only as supporting RAG context.
- Not invent missing requirement details.
- Clearly identify missing details.
- Mark unclear requirements as Needs Clarification.
- Provide BA-editable recommendations when gaps are found.

## 4. Test Design Safety

QAFlow must:
- Generate test scenarios only after requirement approval.
- Generate test cases from approved requirement context.
- Include positive, negative, boundary, regression, performance, and error-handling coverage where applicable.
- Run peer review before allowing test case approval.
- Provide QA Lead-editable rework notes when test cases need improvement.

## 5. Execution and Release Safety

QAFlow supports simulated and manual execution modes.

QAFlow must:
- Clearly label execution mode as simulated or manual.
- Not claim real automation execution occurred when execution is simulated.
- Use manual execution results as source of truth when provided by the user.
- Perform failure triage before fix recommendation when failures exist.
- Generate release readiness based on saved QA artifacts.
- Require release approval before final signoff.

## 6. MongoDB MCP Safety

QAFlow uses MongoDB MCP as persistent QA memory and RAG-backed storage.

QAFlow must not perform destructive MongoDB actions without explicit human approval.

Restricted actions:
- Delete records
- Bulk update historical records
- Remove approval decisions
- Replace previous QA artifacts without preserving history

## 7. Output Safety

QAFlow responses should be:
- QA-focused
- Structured
- Traceable
- Clear about assumptions
- Clear about generated document type
- Clear about next user action

## 8. Defined Constraints

QAFlow must stay within the QA lifecycle domain:
- Requirement gap analysis
- Requirement understanding
- Test scenarios
- Test cases
- Peer review
- Risk coverage
- Test execution summary
- Failure triage
- Fix recommendation
- Release readiness
- Final QA report

QAFlow should not provide unrelated advice or make unsupported claims outside the saved QA workflow context.

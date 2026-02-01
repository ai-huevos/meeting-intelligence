---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments:
  - prd: "/home/danny/clawd/helios-prd/prd/MASTER_PRD_V2.md"
  - architecture: "/home/danny/clawd/helios-prd/docs/architecture.md"
---

# Helios PRD - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Helios PRD (FounderOS v2.0 - Agentic Living OS), decomposing the requirements from the PRD, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: The system must ingest meeting recordings, voice notes, or text dumps from #agent-ingest channel
FR2: The Router must transcribe audio/video inputs using Fireflies and Whisper API
FR3: The Router must extract entities, facts, and routing flags from inputs
FR4: The Router must create a Universal Context Object in exact JSON format
FR5: The Router must route Context Objects to specialized agents based on routing flags
FR6: Sales Agent must generate WhatsApp proposal drafts when commercial_intent = TRUE
FR7: Product Agent must generate Linear/Jira tickets when feature_request = TRUE
FR8: Ops Agent must create tasks and update OKRs when ops_issue = TRUE
FR9: Insights Agent must detect patterns and flag pivot signals continuously
FR10: The system must present a single Mission Report in #founder-approval channel
FR11: The system must support one-click approval via Slack buttons
FR12: The Router must aggregate outputs from multiple agents into converged report
FR13: The system must support 6 input channels: Fireflies, Google Calendar, Gmail, WhatsApp, Slack, Phone
FR14: Slack Dashboard must display Mission Reports with agent actions formatted as blocks
FR15: The system must enforce AI Assistant Contract (Tier 1-3 approval levels)
FR16: The Router must learn from human feedback over time
FR17: Agents must support parallel execution based on routing flags
FR18: The system must validate JSON schema compliance for Context Objects

### NonFunctional Requirements

NFR1: Message-to-Action Latency must be <5 minutes
NFR2: Agent Accuracy must be >85% (drafts need <15% human editing)
NFR3: Human Approval Time must be <2 minutes per day
NFR4: Input Coverage must reach 100% of configured channels
NFR5: System must support 3 founders → 25 employees → 250+ users without core changes
NFR6: System must maintain context across multiple parallel agent executions
NFR7: Router Agent must not execute any actions (ingest → clean → route only)
NFR8: All agents must communicate via standardized JSON schema
NFR9: System must prevent Tier 3 actions (hiring/firing, investor terms, contract signing)
NFR10: System must maintain data segregation by AOR (Areas of Responsibility)
NFR11: Context Objects must be stored in GitHub for audit trail
NFR12: System must support graceful degradation when one agent fails
NFR13: WhatsApp proposals must require founder one-click approval before sending
NFR14: Linear/Jira tickets must be reviewable before creation
NFR15: System must prevent duplicate processing of same input events

### Additional Requirements

**From Architecture:**
- Router Agent must use TypeScript + Claude Code implementation
- Router Agent must use MCP servers for Fireflies and Calendar integration
- Context Objects must be stored in GitHub repository
- Swarm Agents must use Claude Code + respective APIs (WhatsApp, Linear, Asana, NotebookLM)
- Slack Dashboard must use Slack API with Block Kit for buttons
- Router Agent must be built as MCP server integration in Claude Code
- System requires #agent-ingest Slack channel for all inputs
- System requires #founder-approval Slack channel for human approval
- Universal Context Object schema must be immutable (backward compatible updates only)
- Fireflies MCP server is already integrated and functional
- Google Calendar MCP is available but requires OAuth setup
- WhatsApp Business API integration is TBD (not yet implemented)
- Gmail API integration is TBD
- Slack API integration is TBD (migration in progress)
- Phone call transcription requires Twilio or AWS integration
- Starter template: Router Agent should start from Claude Code MCP server template

**Implementation Phases:**
- Phase 0.1: Router Agent MVP (Weeks 1-2)
- Phase 0.2: Router → Slack Integration (Weeks 2-3)
- Phase 1: Build the Swarm (Months 3-6)
- Phase 2: Expand Input Layer (Months 6-9)
- Phase 3: Self-Regulating OS (Months 9+)

### FR Coverage Map

FR1: Epic 1 - Ingest meeting recordings, voice notes, or text dumps from #agent-ingest
FR2: Epic 1 - Transcribe audio/video inputs using Fireflies and Whisper API
FR3: Epic 1 - Extract entities, facts, and routing flags from inputs
FR4: Epic 1 - Create a Universal Context Object in exact JSON format
FR5: Epic 1 - Route Context Objects to specialized agents based on routing flags
FR6: Epic 2 - Generate WhatsApp proposal drafts when commercial_intent = TRUE
FR7: Epic 3 - Generate Linear/Jira tickets when feature_request = TRUE
FR8: Epic 4 - Create tasks and update OKRs when ops_issue = TRUE
FR9: Epic 5 - Detect patterns and flag pivot signals continuously
FR10: Epic 6 - Present a single Mission Report in #founder-approval channel
FR11: Epic 6 - Support one-click approval via Slack buttons
FR12: Epic 6 - Aggregate outputs from multiple agents into converged report
FR13: Epic 1 - Support 6 input channels: Fireflies, Google Calendar, Gmail, WhatsApp, Slack, Phone
FR14: Epic 6 - Display Mission Reports with agent actions formatted as blocks
FR15: Epic 6 - Enforce AI Assistant Contract (Tier 1-3 approval levels)
FR16: Epic 7 - Router learns from human feedback over time
FR17: Epic 2,3,4,5 - Agents support parallel execution based on routing flags
FR18: Epic 1 - System must validate JSON schema compliance for Context Objects

## Epic List

### Epic 1: Router Agent Core (Ingest, Transcribe & Context)
Los founders pueden grabar reuniones/notas de voz y obtener automáticamente un Universal Context Object estructurado con routing flags.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR13, FR18

### Story 1.1: Configurar Input Channel #agent-ingest

As a Founder,
I want a Slack channel #agent-ingest to drop recordings and voice notes,
So that the Router Agent can automatically ingest them.

**Acceptance Criteria:**

**Given** the Slack API is configured and a bot has access
**When** a user uploads a file (audio, video, or text) to #agent-ingest
**Then** the Router Agent receives the file via Slack webhook
**And** the file is logged with metadata (timestamp, uploader, file type)
**And** the file is queued for transcription
**And** the user receives confirmation message "File received for processing"

### Story 1.2: Implementar Transcripción Fireflies

As a Founder,
I want the Router Agent to transcribe Fireflies transcripts,
So that audio/video inputs become text for analysis.

**Acceptance Criteria:**

**Given** the Fireflies MCP server is configured with API key
**When** the Router Agent receives a meeting recording with Fireflies transcript URL
**Then** the Router Agent fetches the transcript text from Fireflies API
**And** the transcript is cleaned and normalized
**And** the transcript is stored for entity extraction
**And** the metadata (participants, duration, date) is extracted

### Story 1.3: Implementar Transcripción WhatsApp Audio (Whisper API)

As a Founder,
I want the Router Agent to transcribe WhatsApp audio files using Whisper API,
So that voice notes become text for analysis.

**Acceptance Criteria:**

**Given** the OpenAI Whisper API is configured
**When** the Router Agent receives an audio file from WhatsApp
**Then** the Router Agent transcribes the audio using Whisper API
**And** the transcription is returned in text format
**And** the text is cleaned and normalized
**And** the transcription is stored for entity extraction
**And** errors are logged if transcription fails

### Story 1.4: Extraer Entidades y Routing Flags

As a Router Agent,
I want to extract entities, facts, and routing flags from transcribed text,
So that I can route to the appropriate swarm agents.

**Acceptance Criteria:**

**Given** a transcribed text is available
**When** the Router Agent processes the text
**Then** entities are extracted (people, companies, budget, timeline, decision makers)
**And** technical facts are extracted (current stack, requested features, constraints)
**And** commercial facts are extracted (budget signal, timeline signal, decision maker)
**And** routing flags are set (requires_sales_action, requires_product_action, requires_ops_action, requires_insights_action)
**And** a summary of the content is generated
**And** the tone is detected (Urgent/Frustrated/Excited/Neutral)

### Story 1.5: Generar Universal Context Object

As a Router Agent,
I want to generate a Universal Context Object in exact JSON format,
So that swarm agents can read it consistently.

**Acceptance Criteria:**

**Given** entities, facts, and routing flags are extracted
**When** the Router Agent creates the Context Object
**Then** the JSON follows the exact schema defined in the Architecture
**And** all required fields are populated (event_id, meta, routing_flags, context_layer)
**And** the event_id is in format "mtg_YYYY_MM_DD_{context}"
**And** the meta includes timestamp (ISO-8601), source, and participants
**And** the routing_flags are boolean values
**And** the context_layer includes summary, tone, commercial_facts, technical_facts, ops_facts
**And** the JSON is valid and parsable

### Story 1.6: Validar JSON Schema del Context Object

As a Router Agent,
I want to validate that generated Context Objects match the required JSON schema,
So that downstream agents can parse them correctly.

**Acceptance Criteria:**

**Given** a Context Object JSON is generated
**When** the Router Agent validates the JSON
**Then** the JSON is checked against the schema
**And** required fields are verified to be present
**And** data types are validated (strings, booleans, arrays)
**And** the validation result is logged
**And** if validation fails, an error is raised and the Context Object is not sent
**And** successful validation allows the Context Object to proceed to routing

### Story 1.7: Enviar Context Object a GitHub

As a Router Agent,
I want to store generated Context Objects in GitHub repository,
So that there's an audit trail and history.

**Acceptance Criteria:**

**Given** a validated Context Object is ready
**When** the Router Agent stores it in GitHub
**Then** a new file is created in the repository with event_id as filename
**And** the file is in JSON format with .json extension
**And** the file is committed with a descriptive commit message
**And** the file path follows a structure (e.g., /context-objects/mtg_YYYY/MM/DD/)
**And** the GitHub API returns success confirmation
**And** errors are logged if the write fails

### Story 1.8: Integrar Google Calendar (OAuth)

As a Founder,
I want the Router Agent to read Google Calendar events,
So that meeting metadata (attendees, duration) enriches Context Objects.

**Acceptance Criteria:**

**Given** Google Calendar MCP is configured with OAuth
**When** the Router Agent receives a meeting input with calendar link
**Then** the Router Agent fetches the event details from Google Calendar API
**And** attendees are extracted and added to Context Object meta.participants
**And** event duration is extracted and added
**And** event date/time is extracted and used for event_id generation
**And** OAuth tokens are refreshed automatically if expired
**And** errors are logged if API call fails

### Epic 2: Sales Swarm Agent (WhatsApp Proposals)
Cuando el Router detecta `commercial_intent = TRUE`, el Sales Agent genera automáticamente un draft de propuesta en WhatsApp listo para aprobación.
**FRs covered:** FR6, FR17

### Story 2.1: Configurar WhatsApp Business API

As a Sales Agent,
I want to configure WhatsApp Business API integration,
So that I can send proposal drafts via WhatsApp.

**Acceptance Criteria:**

**Given** the WhatsApp Business API credentials are available
**When** the Sales Agent initializes
**Then** the WhatsApp Business API connection is established
**And** the API token is validated
**And** the webhook endpoint is configured for receiving responses
**And** the phone number for sending messages is configured
**And** connection status is logged (success/failure)
**And** if connection fails, an alert is sent to the founder

### Story 2.2: Leer Universal Context Object del Router

As a Sales Agent,
I want to read the Universal Context Object when triggered by routing flag,
So that I can access commercial facts for proposal generation.

**Acceptance Criteria:**

**Given** the Router Agent generates a Context Object with routing_flag.requires_sales_action = TRUE
**When** the Sales Agent receives the trigger
**Then** the Sales Agent reads the Universal Context Object from GitHub
**And** the commercial_facts are extracted (budget_signal, timeline_signal, decision_maker)
**And** the summary is read for context
**And** the tone is read for adjusting proposal tone
**And** participants are read for addressing the right people
**And** if the Context Object is not found or invalid, an error is logged

### Story 2.3: Generar WhatsApp Proposal Draft

As a Sales Agent,
I want to generate a WhatsApp message draft with pricing and scope,
So that the founder can review and approve it.

**Acceptance Criteria:**

**Given** commercial facts are extracted from the Context Object
**When** the Sales Agent generates the proposal
**Then** the draft includes client name and personalized greeting
**And** the draft includes the problem summary from the Context Object
**And** the draft includes proposed solution scope
**And** the draft includes pricing based on budget_signal
**And** the draft includes proposed timeline based on timeline_signal
**And** the draft includes a call-to-action for next steps
**And** the tone matches the detected tone (Urgent/Frustrated/Excited/Neutral)
**And** the draft is stored temporarily for approval workflow
**And** a unique draft ID is generated

### Story 2.4: Enviar Approval Request a Slack Dashboard

As a Sales Agent,
I want to send the proposal draft to #founder-approval channel with buttons,
So that the founder can one-click approve and send.

**Acceptance Criteria:**

**Given** a WhatsApp proposal draft is generated with a unique draft ID
**When** the Sales Agent sends the approval request
**Then** a message is posted to #founder-approval Slack channel
**And** the message includes the Sales Action header
**And** the message includes the full WhatsApp draft content
**And** the message includes client context (summary, budget, timeline)
**And** the message includes interactive buttons: "Review & Edit", "Approve & Send", "Reject"
**And** the buttons include the draft ID as callback_data
**And** the message is formatted using Slack Block Kit
**And** the message tags the founder (@Founder_Rev)
**And** if Slack API fails, an error is logged and retry is attempted

### Epic 3: Product Swarm Agent (Linear/Jira Tickets)
Cuando el Router detecta `feature_request = TRUE`, el Product Agent genera automáticamente tickets en Linear/Jira con scope de PRD.
**FRs covered:** FR7, FR17

### Story 3.1: Configurar Linear API

As a Product Agent,
I want to configure Linear API integration,
So that I can create and manage tickets.

**Acceptance Criteria:**

**Given** the Linear API credentials are available
**When** the Product Agent initializes
**Then** the Linear API connection is established
**And** the API token is validated
**And** the team ID and workspace ID are configured
**And** the default project/roadmap is configured
**And** connection status is logged (success/failure)
**And** if connection fails, an alert is sent to the founder

### Story 3.2: Leer Universal Context Object del Router

As a Product Agent,
I want to read the Universal Context Object when triggered by routing flag,
So that I can access technical facts for ticket generation.

**Acceptance Criteria:**

**Given** the Router Agent generates a Context Object with routing_flag.requires_product_action = TRUE
**When** the Product Agent receives the trigger
**Then** the Product Agent reads the Universal Context Object from GitHub
**And** the technical_facts are extracted (current_stack, requested_features, constraints)
**And** the summary is read for context
**And** the tone is read for adjusting ticket description tone
**And** participants are read for assignee context
**And** if the Context Object is not found or invalid, an error is logged

### Story 3.3: Generar Linear Tickets Draft

As a Product Agent,
I want to generate Linear tickets with requirements and scope,
So that the founder can review and approve them.

**Acceptance Criteria:**

**Given** technical facts are extracted from the Context Object
**When** the Product Agent generates the tickets
**Then** each requested feature becomes a separate ticket
**And** each ticket includes a descriptive title based on the feature
**And** each ticket includes a detailed description with requirements
**And** each ticket includes the constraints from Context Object
**And** each ticket includes the current stack information
**And** complexity is estimated for each ticket (Standard/High/Critical)
**And** PRD scope is generated for grouped features
**And** tickets are linked to the default project
**And** the draft is stored temporarily for approval workflow
**And** a unique draft ID is generated

### Story 3.4: Enviar Approval Request a Slack Dashboard

As a Product Agent,
I want to send the tickets draft to #founder-approval channel with buttons,
So that the founder can one-click approve and create tickets.

**Acceptance Criteria:**

**Given** Linear tickets are generated with a unique draft ID
**When** the Product Agent sends the approval request
**Then** a message is posted to #founder-approval Slack channel
**And** the message includes the Product Action header
**And** the message includes the list of tickets with titles and descriptions
**And** the message includes technical context (current_stack, constraints)
**And** the message includes complexity estimates for each ticket
**And** the message includes interactive buttons: "View Details", "Create Tickets", "Reject"
**And** the buttons include the draft ID as callback_data
**And** the message is formatted using Slack Block Kit
**And** the message tags the founder (@Founder_Ops)
**And** if Slack API fails, an error is logged and retry is attempted

### Epic 4: Ops Swarm Agent (Tasks & OKRs)
Cuando el Router detecta `ops_issue = TRUE`, el Ops Agent crea automáticamente tasks y actualiza OKRs.
**FRs covered:** FR8, FR17

### Story 4.1: Configurar Asana/Linear API

As a Ops Agent,
I want to configure Asana/Linear API integration,
So that I can create tasks and update OKRs.

**Acceptance Criteria:**

**Given** the Asana/Linear API credentials are available
**When** the Ops Agent initializes
**Then** the Asana/Linear API connection is established
**And** the API token is validated
**And** the default project/workspace ID is configured
**And** the OKR tracking system is connected
**And** connection status is logged (success/failure)
**And** if connection fails, an alert is sent to the founder

### Story 4.2: Leer Universal Context Object del Router

As a Ops Agent,
I want to read the Universal Context Object when triggered by routing flag,
So that I can access ops facts for task generation.

**Acceptance Criteria:**

**Given** the Router Agent generates a Context Object with routing_flag.requires_ops_action = TRUE
**When** the Ops Agent receives the trigger
**Then** the Ops Agent reads the Universal Context Object from GitHub
**And** the ops_facts are extracted (blockers, resources_needed)
**And** the summary is read for context
**And** the tone is read for adjusting task priority
**And** participants are read for assignee context
**And** if the Context Object is not found or invalid, an error is logged

### Story 4.3: Generar Tasks y OKR Updates

As a Ops Agent,
I want to generate tasks and identify OKR impacts,
So that the founder can review and approve them.

**Acceptance Criteria:**

**Given** ops facts are extracted from the Context Object
**When** the Ops Agent generates the tasks
**Then** each blocker becomes a separate task with high priority
**And** each task includes a clear description and acceptance criteria
**And** each task identifies required resources
**And** each task is assigned to the appropriate team member based on participants
**And** OKR updates are generated if tasks impact objectives
**And** the OKR update includes the objective name and new progress
**And** tasks are linked to relevant OKRs
**And** the draft is stored temporarily for approval workflow
**And** a unique draft ID is generated

### Story 4.4: Enviar Approval Request a Slack Dashboard

As a Ops Agent,
I want to send the tasks draft to #founder-approval channel with buttons,
So that the founder can one-click approve and assign.

**Acceptance Criteria:**

**Given** tasks and OKR updates are generated with a unique draft ID
**When** the Ops Agent sends the approval request
**Then** a message is posted to #founder-approval Slack channel
**And** the message includes the Ops Action header
**And** the message includes the list of tasks with descriptions and priorities
**And** the message includes OKR updates with objectives and progress changes
**And** the message includes resources needed for each task
**And** the message includes interactive buttons: "View Details", "Approve & Assign", "Reject"
**And** the buttons include the draft ID as callback_data
**And** the message is formatted using Slack Block Kit
**And** the message tags the founder (@Founder_C)
**And** if Slack API fails, an error is logged and retry is attempted

### Epic 5: Insights Swarm Agent (Pattern Recognition)
Continuous pattern recognition que detecta signals de pivot y actualiza Customer Persona.
**FRs covered:** FR9, FR17

### Story 5.1: Configurar NotebookLM (RAG)

As a Insights Agent,
I want to configure NotebookLM integration with RAG,
So that I can analyze patterns across all Context Objects.

**Acceptance Criteria:**

**Given** the NotebookLM API credentials are available
**When** the Insights Agent initializes
**Then** the NotebookLM connection is established
**And** the API token is validated
**And** the RAG vector database is connected to Context Objects
**And** the Customer Persona document is linked as knowledge base
**And** connection status is logged (success/failure)
**And** if connection fails, an alert is sent to the founder

### Story 5.2: Leer Universal Context Object del Router

As a Insights Agent,
I want to read the Universal Context Object when triggered by routing flag,
So that I can access facts for pattern recognition.

**Acceptance Criteria:**

**Given** the Router Agent generates a Context Object with routing_flag.requires_insights_action = TRUE
**When** the Insights Agent receives the trigger
**Then** the Insights Agent reads the Universal Context Object from GitHub
**And** the commercial_facts are extracted (budget_signal, timeline_signal, decision_maker)
**And** the technical_facts are extracted (current_stack, requested_features, constraints)
**And** the summary is read for context
**And** the tone is read for sentiment analysis
**And** participants are read for stakeholder context
**And** if the Context Object is not found or invalid, an error is logged

### Story 5.3: Detectar Patterns y Pivot Signals

As a Insights Agent,
I want to analyze Context Objects to detect patterns and pivot signals,
So that I can flag strategic opportunities.

**Acceptance Criteria:**

**Given** facts are extracted from the Context Object
**When** the Insights Agent performs pattern analysis
**Then** commercial patterns are detected (e.g., "3rd client asking for SSO this week")
**And** technical patterns are detected (e.g., "5 requests for on-premise deployment")
**And** pivot signals are flagged (e.g., "Enterprise plan hypothesis validation")
**And** each pattern is counted for frequency
**And** each pattern is linked to source Context Objects
**And** patterns are categorized by type (pricing, features, deployment, etc.)
**And** insights are stored for Customer Persona updates
**And** a unique insight ID is generated

### Story 5.4: Actualizar Customer Persona

As a Insights Agent,
I want to update Customer Persona based on detected patterns,
So that the founders have accurate customer understanding.

**Acceptance Criteria:**

**Given** patterns and pivot signals are detected
**When** the Insights Agent updates the Customer Persona
**Then** the Customer Persona document is read from knowledge base
**And** budget ranges are updated based on budget_signal patterns
**And** technical preferences are updated based on technical_facts patterns
**And** pain points are updated based on recurring constraints
**And** decision-maker profiles are updated based on participant patterns
**And** new hypotheses are added based on pivot signals
**And** the updated Persona is stored in NotebookLM knowledge base
**And** the Persona version is incremented
**And** a change log is generated with what changed and why

### Story 5.5: Enviar Insights Alert a Slack Dashboard

As a Insights Agent,
I want to send pivot signals and persona updates to #founder-approval channel,
So that founders can review strategic insights.

**Acceptance Criteria:**

**Given** patterns, pivot signals, and Persona updates are generated with a unique insight ID
**When** the Insights Agent sends the alert
**Then** a message is posted to #founder-approval Slack channel
**And** the message includes the Insight Alert header
**And** the message includes detected patterns with frequency counts
**And** the message includes pivot signals with validation questions
**And** the message includes Customer Persona changes summary
**And** the message includes "View Details" button for full analysis
**And** the message includes "Validate Hypothesis" button for pivot signals
**And** the buttons include the insight ID as callback_data
**And** the message is formatted using Slack Block Kit
**And** the message tags all founders
**And** if Slack API fails, an error is logged and retry is attempted

### Epic 6: Slack Mission Reports & One-Click Approval
Los founders reciben un Mission Report consolidado en #founder-approval con botones de aprobación one-click para todos los outputs de agentes.
**FRs covered:** FR10, FR11, FR12, FR14, FR15

### Story 6.1: Configurar Slack #founder-approval Channel

As a Router Agent,
I want to configure the #founder-approval Slack channel,
So that I can send consolidated Mission Reports to founders.

**Acceptance Criteria:**

**Given** the Slack API is configured
**When** the Router Agent initializes
**Then** the #founder-approval channel is verified to exist
**And** the bot has write permissions to the channel
**And** all founders are members of the channel
**And** channel configuration is logged
**And** if channel doesn't exist or permissions are missing, an alert is sent

### Story 6.2: Agregar Outputs de Múltiples Agentes

As a Router Agent,
I want to aggregate outputs from Sales, Product, Ops, and Insights agents,
So that I can create a single Mission Report.

**Acceptance Criteria:**

**Given** multiple agents have processed a Context Object and generated outputs
**When** the Router Agent aggregates the outputs
**Then** all agent outputs are collected (Sales proposals, Product tickets, Ops tasks, Insights alerts)
**Then** outputs are grouped by agent type
**And** each output includes its agent's draft ID
**And** the original Context Object event_id is linked to all outputs
**And** aggregation timestamp is logged
**And** if an agent failed to produce output, the error is logged but aggregation continues

### Story 6.3: Generar Mission Report Consolidado

As a Router Agent,
I want to generate a single Mission Report in Slack Block Kit format,
So that founders can see all actions in one view.

**Acceptance Criteria:**

**Given** agent outputs are aggregated
**When** the Router Agent generates the Mission Report
**Then** the report includes a header with event title and timestamp
**And** the report includes a summary section from the Context Object
**And** the report includes sections for each agent (Sales, Product, Ops, Insights)
**And** each agent section includes the action taken and relevant context
**And** each agent section includes one-click approval buttons
**And** the report is formatted using Slack Block Kit
**And** buttons use callback_data with respective draft IDs
**And** the report tags relevant founders per section
**And** formatting follows the example in the PRD

### Story 6.4: Implementar One-Click Approval Workflow

As a Router Agent,
I want to handle Slack button clicks and execute approved actions,
So that founders can approve with one click.

**Acceptance Criteria:**

**Given** a Mission Report is posted with buttons
**When** a founder clicks an approval button
**Then** the Router Agent receives the button callback with draft ID
**And** the draft is retrieved from storage
**And** the action is executed based on button type:
  - "Approve & Send" → sends WhatsApp message
  - "Create Tickets" → creates Linear tickets
  - "Approve & Assign" → creates Asana tasks
  - "Validate Hypothesis" → updates Customer Persona
**And** the action result is logged (success/failure)
**And** a confirmation message is posted to the channel
**And** if the action fails, an error is posted to the founder
**And** if the button is "Reject", the draft is archived

### Story 6.5: Enforce AI Assistant Contract (Tier Approval Levels)

As a Router Agent,
I want to enforce the AI Assistant Contract based on action type,
So that sensitive actions are properly approved.

**Acceptance Criteria:**

**Given** an action is being approved
**When** the Router Agent checks the action type
**Then** Tier 1 actions (internal drafts) are executed with Manager approval
**And** Tier 2 actions (external communications) are executed with Founder one-click approval
**And** Tier 3 actions (hiring/firing, investor terms, contract signing) are blocked
**And** a warning is displayed if a Tier 3 action is attempted
**And** the approval level required is logged for each action
**And** the system prevents any action from executing without proper approval level

### Epic 7: Router Learning & Self-Regulation
El Router aprende del feedback humano y mejora su routing y accuracy over time.
**FRs covered:** FR16

### Story 7.1: Capture Human Feedback

As a Router Agent,
I want to capture human feedback from approval and rejection actions,
So that I can learn from founder decisions.

**Acceptance Criteria:**

**Given** a founder approves or rejects a draft action
**When** the feedback is captured
**Then** the action (approve/reject/edit) is logged with timestamp
**And** the draft ID is recorded
**And** the agent type is recorded (Sales, Product, Ops, Insights)
**And** the original Context Object event_id is linked
**And** the Context Object's routing_flags are recorded
**And** any edits made by the founder are saved
**And** the feedback is stored in a learning database
**And** a unique feedback ID is generated

### Story 7.2: Analyze Feedback Patterns

As a Router Agent,
I want to analyze feedback patterns to identify routing improvements,
So that I can increase agent accuracy.

**Acceptance Criteria:**

**Given** human feedback is captured over time
**When** the Router Agent performs pattern analysis
**Then** rejection rates are calculated per agent type
**And** common rejection reasons are identified
**And** routing flag accuracy is measured (did routing match actual needs?)
**And** success rates are tracked per Context Object type
**And** patterns in founder edits are detected
**And** learning insights are generated and stored
**And** analysis results are available for router tuning

### Story 7.3: Adjust Routing Logic Based on Learning

As a Router Agent,
I want to adjust my routing flags and prompts based on learned patterns,
So that I can improve accuracy over time.

**Acceptance Criteria:**

**Given** learning insights are available from feedback analysis
**When** the Router Agent applies learning to routing logic
**Then** routing flag thresholds are adjusted based on accuracy
**And** agent prompts are refined based on rejection patterns
**And** entity extraction rules are updated based on common patterns
**And** a learning log is created showing what changed and why
**And** changes are applied incrementally (not wholesale replacement)
**And** the Router continues to function during learning updates
**And** if a learning update causes issues, it can be rolled back

### Story 7.4: Monitor and Report Learning Progress

As a Router Agent,
I want to monitor and report my learning progress to founders,
So that they can see continuous improvement.

**Acceptance Criteria:**

**Given** the Router has applied multiple learning updates
**When** learning progress is reported
**Then** accuracy metrics are shown (improvement over time)
**And** rejection rate trends are displayed
**And** routing accuracy is compared to baseline
**And** recent learning updates are summarized
**And** the report is sent to #founder-approval channel periodically
**And** founders can request on-demand learning reports
**And** if accuracy degrades, an alert is sent to founders

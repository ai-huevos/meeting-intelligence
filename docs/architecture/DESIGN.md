# Meeting Intelligence System Design

## 1. High-Level Architecture
This system ingests meeting contexts, processes them via AI agents, and outputs actionable insights to CRM and messaging platforms.

```mermaid
graph TD
    %% Global Styles for Dark Mode / Neon
    classDef pink fill:none,stroke:#ff00ff,stroke-width:2px,color:#fff;
    classDef cyan fill:none,stroke:#00ffff,stroke-width:2px,color:#fff;
    classDef lime fill:none,stroke:#00ff00,stroke-width:2px,color:#fff;
    classDef yellow fill:none,stroke:#ffff00,stroke-width:2px,color:#fff;
    classDef white fill:none,stroke:#ffffff,stroke-width:1px,color:#fff,stroke-dasharray: 5 5;

    %% --- Layer 1: The User Journey (Omnichannel) ---
    subgraph User_Touchpoints ["User Touchpoints"]
        direction TB
        User(("User / Sales Rep")):::pink
        
        %% Channels
        Meta[("WhatsApp (Kapso)")]:::pink
        Slack_TP[("Slack")]:::pink
        GCal[("Google Calendar")]:::pink
        Fireflies[("Fireflies.ai")]:::pink
    end

    %% Flow: Interaction
    User -->|Chat / Query| Meta
    User -->|Slash Command| Slack_TP
    User -->|Schedules| GCal
    User -->|Attends Meeting| Fireflies

    %% --- Layer 2: Ingestion & Triggers ---
    subgraph Ingestion ["Ingestion Layer"]
        Webhook_H[("/webhook Endpoint")]:::cyan
        Transcript_H[("/transcript Endpoint")]:::cyan
        Daily_Trigger[("Daily Scheduler")]:::cyan
    end

    Meta -->|"Incoming Msg"| Webhook_H
    Slack_TP -->|"Command/Event"| Webhook_H
    Fireflies -->|"New Transcript"| Transcript_H
    GCal -->|"Event Scheduled"| Daily_Trigger

    %% --- Layer 3: Intelligence Core ---
    subgraph Intelligence_Core ["Meeting OS Core"]
        direction TB
        
        Router{{"Router Agent"}}:::yellow
        
        %% Agents
        SalesAg["Sales Agent"]:::cyan
        OpsAg["Ops Agent"]:::cyan
        ResAg["Research Agent"]:::cyan
        
        %% Services
        Workflow["n8n Workflow Engine"]:::cyan
    end
    
    %% All triggers go to Router
    Webhook_H --> Router
    Transcript_H --> Router
    Daily_Trigger --> Router

    %% Routing Logic
    Router -->|"Sales Context"| SalesAg
    Router -->|"Operational"| OpsAg
    Router -->|"Research Req"| ResAg

    %% Dependencies
    SalesAg -.->|"Extract Deal Info"| Workflow
    ResAg -.->|"Enrich Participants"| Workflow
    OpsAg -.->|"Task extraction"| Workflow

    %% --- Layer 4: Cognitive Services (LLMs) ---
    subgraph Brain ["Cognitive Services"]
        Gemini(("&nbsp;&nbsp;Gemini 1.5&nbsp;&nbsp;")):::white
        Perplexity(("&nbsp;&nbsp;Perplexity&nbsp;&nbsp;")):::white
    end

    Workflow <-->|"Reasoning & Extraction"| Gemini
    ResAg <-->|"Live Web Search"| Perplexity

    %% --- Layer 5: Effectors & Outcomes (End) ---
    subgraph Effectors ["Outcomes & External Systems"]
        Notion_CRM[("Notion (CRM & KB)")]:::lime
        Slack_Out[("Slack Alerts")]:::lime
        KapsoReply[("WhatsApp Reply")]:::lime
    end

    Workflow -->|"Update CRM / KB"| Notion_CRM
    Workflow -->|"Notify Team"| Slack_Out
    
    %% Loop back to user
    SalesAg -->|"Auto-Reply"| KapsoReply
    KapsoReply -->|"Forward to User"| Meta
    
    %% Implicit Flow for Viz
    ResAg -->|"Morning Briefing"| Slack_Out
```

## 2. Component Flow: Kapso Integration
Detailing the WhatsApp communication flow.

```mermaid
sequenceDiagram
    participant User
    participant Kapso(Proxy)
    participant Meta(WhatsApp)
    participant MeetingOS

    User->>Meta: "Hello" (Starts Session)
    Meta->>Kapso: Webhook
    Kapso->>MeetingOS: POST /webhook
    MeetingOS->>MeetingOS: Log Event
    
    MeetingOS->>Kapso: POST /messages (Replier)
    Kapso->>Meta: Forward Request
    Meta->>User: "Ack Received"
```

## 3. Data Pipeline (E2E)
Structure of the data flowing through the system.

```mermaid
classDiagram
    class Meeting {
        +String id
        +Date start_time
        +List attendees
        +String transcript_text
    }
    
    class Enrichment {
        +String target_company
        +List news_articles
        +String summary
    }
    
    class Outcome {
        +List action_items
        +String sentiment
        +String next_steps
    }
    
    Meeting --> Enrichment : User Prep
    Meeting --> Outcome : Post-Meeting
```

## 4. Workflow Engine (n8n Agent Logic)

The **Workflow Engine** (n8n) acts as the execution arm for complex, multi-step business logic. It orchestrates the flow of data between the Router, LLMs, and external systems (Notion, CRM).

**Example: Sales Agent Workflow**
This diagram illustrates the internal logic of the `Sales_Agent_Workflow` (defined in `meeting_os/sales_workflow.json`).

```mermaid
graph TD
    %% Styling
    classDef trigger fill:#2d333b,stroke:#00ffff,stroke-width:2px,color:#fff;
    classDef action fill:#2d333b,stroke:#00ff00,stroke-width:2px,color:#fff;
    classDef llm fill:#2d333b,stroke:#ff00ff,stroke-width:2px,color:#fff;
    classDef db fill:#2d333b,stroke:#ffff00,stroke-width:2px,color:#fff,stroke-dasharray: 5 5;

    %% Nodes
    In([Webhook Trigger]):::trigger
    
    subgraph Logic ["Extraction & Reasoning"]
        Gemini[("Gemini 1.5 Pro")]:::llm
    end

    subgraph Actions ["Side Effects (Parallel)"]
        CreateOpp[["Create/Update Opportunity"]]:::action
        CreateComp[["Create/Update Company"]]:::action
    end
    
    NotionDB[("Notion Database")]:::db

    %% Relationships
    In -- "Raw Transcript" --> Gemini
    
    Gemini -- "Extracted Deal Info (JSON)" --> CreateOpp
    Gemini -- "Extracted Company Info (JSON)" --> CreateComp
    
    CreateOpp -.-> NotionDB
    CreateComp -.-> NotionDB

    %% Data Annotations
    note_gemini["> Extracts:\n- Client Name\n- Deal Value\n- Stage\n- Probability\n- Key People\n- Next Steps"]
    Gemini -.- note_gemini
```

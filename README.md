# llm-historical-pricing

LLM cost per token history

flowchart TB
    A[100 Requests Arrive<br/>Simultaneously]

    A --> B[Azure Load Balancer<br/> Round-Robin]

    B -->|50 requests| C[Instance 1]
    B -->|50 requests| D[Instance 2]

    subgraph I1 [Instance 1]
        C --> C1[Semaphore 20]
        C1 --> C2[Processing: 20]
        C1 --> C3[Waiting: 30]
        C1 --> C4[Total: 50]
    end

    subgraph I2 [Instance 2]
        D --> D1[Semaphore 20]
        D1 --> D2[Processing: 20]
        D1 --> D3[Waiting: 30]
        D1 --> D4[Total: 50]
    end

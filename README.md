# WeCode-Ai-Learning-Assistant

This is an ai assistant which uses the socratic method of questioning for teaching in any topic in DSA and could and can explain any complex topic. The Model can dynamically understand the expertise level of the user of a given topic and the model can change the perception of the user if they explicitly say so. the default learning technique is socratic method.there is 1 more additonal learning method which the user can choose from which is Feynman Technique .Also most importantly the user can define and create a custom learning or teaching method of their own.The user

---
Complete System Architecture

'''mermaid
graph TB
    subgraph User Interface
        A[User Input] --> B[Main Interaction Loop]
        B --> C[Display AI Response]
    end

    subgraph AI Models
        D[AiModel]
        D --> |Inherits| E[SentimentModel]
        D --> |Inherits| F[SocraticModel]
        D --> |Inherits| G[FeynmanModel]
        D --> |Inherits| H[CustomModel]
    end

    subgraph Model Switching Logic
        I[Current Model] --> J{Score < -2?}
        J -->|Yes| K[Switch Model]
        J -->|No| I
        K --> L{Is Custom?}
        L -->|Yes| M[Prompt for Instructions]
        L -->|No| I
    end

    subgraph Database Operations
        N[(SQLite Database)]
        O[Initialize DB] --> N
        P[Save Chat History] --> N
        Q[Update Sentiment] --> N
        R[Get Chat by Category] --> N
    end

    subgraph Chat Categorization
        S[New Chat Entry] --> T{Categorize}
        T --> U[Today]
        T --> V[Yesterday]
        T --> W[Previous 7 days]
        T --> X[Older]
    end

    B --> E
    B --> I
    I --> F
    I --> G
    I --> H
    B --> P
    B --> Q
    C --> R
    P --> S



---
Class Diagram

'''mermaid
classDiagram
    class AiModel {
        -model
        -chat
        -score
        +__init__(model_name, generation_config, system_instruction)
        +get_response(user_prompt)*
        +update_score(result, current_score, model_name)*
    }
    class SentimentModel {
        +get_result_sentiment(user_prompt)
    }
    class SocraticModel {
        +get_response(user_prompt)
    }
    class FeynmanModel {
        +get_response(user_prompt)
    }
    class CustomModel {
        +get_response(user_prompt)
    }
    AiModel <|-- SentimentModel
    AiModel <|-- SocraticModel
    AiModel <|-- FeynmanModel
    AiModel <|-- CustomModel




---
Code Flow

'''mermaid
graph TD
    A[Start] --> B[Get user prompt]
    B --> C[Perform sentiment analysis]
    C --> D[Generate AI response]
    D --> E[Save chat history]
    E --> F[Update model score]
    F --> G{Score < -2?}
    G -->|Yes| H[Switch to next model]
    G -->|No| B
    H --> I{Is Custom Model?}
    I -->|Yes| J[Ask for custom instructions]
    I -->|No| B
    J --> K{User wants custom?}
    K -->|Yes| L[Set custom instructions]
    K -->|No| M[Switch to Socratic model]
    L --> B
    M --> B




----
Chat History Database Flow

'''mermaid
graph TD
    A[New Chat Entry] --> B{Categorize by Date}
    B -->|Same day| C[Today]
    B -->|Yesterday| D[Yesterday]
    B -->|Within last week| E[Previous 7 days]
    B -->|Older| F[Older]
    
    C --> G[Save to DB]
    D --> G
    E --> G
    F --> G
    
    H[Retrieve Chats] --> I{Select Category}
    I --> J[Fetch Today's Chats]
    I --> K[Fetch Yesterday's Chats]
    I --> L[Fetch Last Week's Chats]
    I --> M[Fetch Older Chats]
    
    J --> N[Display Chats]
    K --> N
    L --> N
    M --> N
    
    subgraph Database
    G --> O[(ChatHistory Table)]
    O --> J
    O --> K
    O --> L
    O --> M
    end
# WeCode-Ai-Learning-Assistant
# GENAI powered teaching assistant

An AI-based tool designed to help users learn complex topics such as Data Structures and Algorithms (DSA). The assistant primarily utilizes the Socratic method of questioning but also includes alternative learning techniques. These techniques can be customized by the user to suit their learning style.

The Model can dynamically understand the expertise level of the user of a given topic and the model can change the perception of the user if they explicitly say so. the default learning technique is socratic method.There is 1 more additonal learning method which the user can choose from which is Feynman Technique .Also most importantly the user can define and create a custom learning or teaching method of their own.The user

---
Complete System Architecture

```mermaid
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
```


---
Class Diagram

```mermaid
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
```




---
visualizes the interaction between users and the AI models in a more emotionally resonant and intuitive way.
## Technical Implementation

The diagram represents a sentiment-driven, adaptive multi-model AI system. Sentiment analysis is performed on each user interaction using a dedicated SentimentModel, quantifying emotional context. A cumulative scoring mechanism (-1 for negative, 0 for neutral, +1 for positive) triggers model switching when the score falls below -2. The system employs three distinct models (Socratic, Feynman, and Custom) with inheritance from a base AiModel class, each implementing unique response generation strategies. The Custom model, when activated, allows for dynamic system instruction updates, enhancing adaptability. This architecture enables continuous learning and optimization based on user interactions and feedback.


```mermaid
%%{init: {'theme': 'dark', 'themeVariables': { 'darkMode': true }}}%%
graph TD
    subgraph "AI Models' Emotional Journey"
        A[Start: Socratic Model] -->|User Interaction| B{Sentiment Analysis}
        B -->|Positive| C[["😊 +1 Score"]]
        B -->|Neutral| D[["😐 No Change"]]
        B -->|Negative| E[["😢 -1 Score"]]
        
        C --> F{Score Check}
        D --> F
        E --> F
        
        F -->|Score >= -2| G[["🧠 Continue Learning"]]
        F -->|Score < -2| H[["😰 Struggle"]]
        
        H -->|Switch Model| I[Feynman Model]
        I --> J[["🔄 Reset Score"]]
        J --> |User Interaction| B
        
        I -->|Multiple Struggles| K[Custom Model]
        K -->|User Accepts| L[["🎨 Customization"]]
        K -->|User Declines| M[["↩️ Return to Socratic"]]
        
        L --> |User Interaction| B
        M --> A
        
        G -->|Continuous Learning| N[["🌟 AI Growth"]]
        N -->|New Challenges| B
    end

    classDef default fill:#2a2a2a,stroke:#7a7a7a,color:#e0e0e0;
    classDef model fill:#4a4a8c,stroke:#7a7aff,color:#ffffff,stroke-width:2px;
    classDef positive fill:#2d6a4f,stroke:#40916c,color:#ffffff;
    classDef neutral fill:#7d6608,stroke:#b7921e,color:#ffffff;
    classDef negative fill:#991b1b,stroke:#dc2626,color:#ffffff;
    classDef action fill:#374151,stroke:#6b7280,color:#ffffff;
    
    class A,I,K model;
    class C positive;
    class D neutral;
    class E negative;
    class G,L,N positive;
    class H negative;
    class B,F,J,M action;
```




---
Code Flow

```mermaid
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
```









---
Chat History Database Flow

```mermaid
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
```
# WeCode-Ai-Learning-Assistant

# GENAI powered teaching assistant

An AI-based tool designed to help users learn complex topics such as Data Structures and Algorithms (DSA). The assistant primarily utilizes the Socratic method of questioning but also includes alternative learning techniques. These techniques can be customized by the user to suit their learning style.


## Features

- Multiple Learning Methods:
    - Socratic Method
    - Feynman Technique
    - User-defined custom learning methods
- Dynamic User Expertise Level:
    - The model can gauge the user’s expertise level and adjust its responses accordingly.
- User Interaction:
    - Users can choose their preferred teaching methods and create their own.



## Learning Techniques

- Socratic Method: Engages users by asking guided questions to deepen understanding.
- Feynman Technique: Simplifies complex ideas to basic concepts, ensuring full comprehension.
- Customizable Methods: Users can design their own teaching methods tailored to their learning style.
## AI Model Architecture

The system relies on a multi-layered model structure that adapts its responses dynamically

```mermaid
classDiagram
    AIModel <|-- SentimentModel
    AIModel <|-- SocraticModel
    AIModel <|-- FeynmanModel
    AIModel <|-- CustomModel
    class AIModel{
        +model
        +chat
        +score
        +get_response(user_prompt)
        +update_score(result)
    }
    class SentimentModel{
        +get_response(user_prompt)
    }
    class SocraticModel{
        +get_response(user_prompt)
    }
    class FeynmanModel{
        +get_response(user_prompt)
    }
    class CustomModel{
        +get_response(user_prompt)
    }
```

### Frameworks and Libraries

Additional frameworks and libraries used in this project:

* ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

* ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

## Installation

1.Clone the repository:

```bash
git clone https://github.com/sky0walker99/WeCode-Ai-Learning.git

```
2.Navigate to the project directory and install dependencies:

```bash
cd WeCode-Ai-Learning
pip install -r requirements.txt

```
3.Run the project
```bash

python main.py

```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY` : https://aistudio.google.com/app/apikey


## 🚀 About Me
This is a collaborative project developed by a team of four passionate individuals:

- ALEN SUNNY       – AI/ML Specialist, responsible for the AI model architecture 
- MUHAMMED HAROON  – AI/ML Specialist, responsible for the AI model architecture and core features
- Muhammed Shahbas – AI/ML Specialist, responsible for the AI model architecture and database integration
- MALIK DINAR A S  – FullStack Developer, focused on the user interface and experience and server-side logic.
- 
Our goal is to create an innovative and interactive platform for teaching complex topics like Data Structures and Algorithms using cutting-edge AI technology.



## 🔗 Links
- AlenSuny :[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Alen-121) 
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alen--sunny/)
- Muhammed Haroon :[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sky0walker99/) 
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/muhammed-haroon-0399962b8/)
- Malik Dinar A S :[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/malik-dinar) 
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/malik-dinar-510795234/)
- Muhammed Shanz :[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Blaacknight)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shahbas-v-s-7055ab2a9/)




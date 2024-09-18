import google.generativeai as genai
from abc import ABC , abstractmethod

# Created a base class (Aimodel) and a subclass of models (socratic,feynman,etc) which inherits from the base class.
class AiModel():
    def __init__(self, model_name, generation_config, system_instruction):
        self.model = genai.GenerativeModel( model_name=model_name,
        generation_config=generation_config,tools="code_execution",
        system_instruction=system_instruction)
        self.chat = self.model.start_chat(history=[])
        self.score = 0
        
    @abstractmethod
    def get_response(self,user_prompt) -> str:
        return self.chat.send_message(user_prompt).text
    
    @abstractmethod
    def update_score(self ,result, current_score, model_name):
        review = ["positive", "neutral", "negative"]
        if result == review[0]:
            current_score += 1
            update_positive_sentiment(model_name)  # Update positive sentiment count in DB
        elif result == review[2]:
            current_score -= 1
        return current_score 
    
class SentimentModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name, generation_config, system_instruction)
    
    def get_result_sentiment(self,user_prompt):
        result = self.chat.send_message(user_prompt).text.strip()
        return result

class SocraticModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name , generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)
    
class FeynmanModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name, generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)
    
class CustomModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name , generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)


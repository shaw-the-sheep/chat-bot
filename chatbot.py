from transformers import AutoModelForCausalLM, AutoTokenizer
from torch import cat

class Chatbot:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        # Load the pre-trained model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.chat_history_ids = None

    def chat(self, user_input):
        # Encode the user input
        new_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors="pt")
        
        # Concatenate new input with chat history (if any)
        if self.chat_history_ids is None:
            self.chat_history_ids = new_input_ids
        else:
            self.chat_history_ids = cat([self.chat_history_ids, new_input_ids], dim=-1)
        
        # Generate a response
        response_ids = self.model.generate(
            self.chat_history_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            top_p=0.95,
            top_k=50
        )
        
        # Decode and return the response
        response = self.tokenizer.decode(response_ids[:, self.chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
        return response

# Instantiate the chatbot
chatbot = Chatbot()

# Chat with the bot
print("Chatbot: Hello! Type 'exit' to end the chat.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Chatbot: Goodbye!")
        break
    response = chatbot.chat(user_input)
    print(f"Chatbot: {response}")

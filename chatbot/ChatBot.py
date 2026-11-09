# chatbot.py
import random
import json
import torch
from . import model
from .nltk_utils import bag_of_words, tokenize

class ChatBot:
    def __init__(self, intents_file, model_file):
        with open(intents_file, 'r') as file:
            self.intents = json.load(file)

        data = torch.load(model_file)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data['all_words']
        tags = data['tags']
        model_state = data["model_state"]

        self.model = model.NeuralNet(input_size, hidden_size, output_size)
        self.model.load_state_dict(model_state)
        self.model.eval()

        self.all_words = all_words
        self.tags = tags

    def get_response(self, question):

        sentence = tokenize(question)
        X = bag_of_words(sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.85:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return random.choice(intent['responses'])
        else:
            return "I apologize, I do not have enough information to answer that yet?"

    with open("intents.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    def format_response(text):
        sentences = text.strip().split(";")
        bulleted_list = []
        for sentence in sentences:
            bulleted_list.append(f"<li>{sentence}</li>")
        return f"<ul>\n{''.join(bulleted_list)}\n</ul>"
    for intent in data["intents"]:
        for i, response in enumerate(intent["responses"]):
            intent["responses"][i] = format_response(response)
    with open("intents.json", "w") as f:
        json.dump(data, f, indent=4) 
    print(data["intents"][0]["responses"][0])  
import random
import json

import torch

from online import search_google
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from correction import fix_spelling_errors

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "C.H.I.M.E"
print("Let's chat! (type 'quit' to exit, 'info' for factual queries)")
while True:
    inp = input("You: ")
    if inp == "quit":
        break
    elif inp == "info":
        while True:
            print("Enter your query (type 'back' to go back)")
            query = input("You (info mode): ")
            if query.lower() == "back":
                break
            snippets = search_google(query)
            if snippets:
                # Tokenize the query to use as context
                context = set(query.split())
                best_snippet = None
                max_overlap = -1

                # Iterate over the snippets and apply Lesk Algorithm
                for snippet in snippets:
                    snippet_tokens = set(snippet.split())
                    overlap = len(context.intersection(snippet_tokens))
                    # Choose snippet with maximum overlap and less than 150 characters
                    if overlap > max_overlap and len(snippet) <= 150:
                        max_overlap = overlap
                        best_snippet = snippet

                print(best_snippet)  # Print the snippet with the highest overlap and length <= 150
            else:
                print("No results found.")

    sentence = fix_spelling_errors(inp)
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else:
        print(f"{bot_name}: I do not understand...")
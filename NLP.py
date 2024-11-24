from nltk.corpus import wordnet

# Function to perform Lesk Algorithm
def lesk_algorithm(context, word):
    best_sense = None
    max_overlap = -1

    # Iterate over all synsets of the target word in WordNet
    for synset in wordnet.synsets(word):
        # Extract the definition of the synset and tokenize it
        definition = synset.definition()
        definition_tokens = set(definition.split())

        # Calculate the overlap between the context and the definition tokens
        overlap = len(set(context).intersection(definition_tokens))

        # Update the best sense if the overlap is greater
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = synset

    return best_sense.definition() if best_sense else None
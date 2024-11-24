from autocorrect import Speller

# Create an instance of the Speller class
spell = Speller(lang='en')

# Function to fix spelling errors in a sentence
def fix_spelling_errors(sentence):
    # Split the sentence into words and fix spelling errors for each word
    corrected_sentence = ' '.join(spell(word) for word in sentence.split())
    return corrected_sentence

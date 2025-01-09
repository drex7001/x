from nltk.util import ngrams
from collections import Counter

# Example text corpus
text = "I like coding in Python. Python is great for data analysis. I also like machine learning."

# Tokenize the text manually (alternative to nltk.word_tokenize)
def tokenize(text):
    return text.lower().split()

# Tokenize the text
words = tokenize(text)

# Generate N-grams (example: bigrams, N=2)
n = 2
bigrams = list(ngrams(words, n))

# Count the frequency of each bigram
bigram_counts = Counter(bigrams)

# Display the bigram counts
print("Bigram Counts:")
for bigram, count in bigram_counts.items():
    print(f"{bigram}: {count}")

# Calculate conditional probabilities
print("\nConditional Probabilities:")
conditional_probabilities = {}
for bigram, count in bigram_counts.items():
    first_word = bigram[0]
    total_count_first_word = sum(c for b, c in bigram_counts.items() if b[0] == first_word)
    probability = count / total_count_first_word
    conditional_probabilities[bigram] = probability
    print(f"P({bigram[1]} | {bigram[0]}) = {probability:.4f}")

# Example of predicting the next word given a word
def predict_next_word(word, ngram_probs):
    candidates = {b[1]: p for b, p in ngram_probs.items() if b[0] == word}
    return max(candidates, key=candidates.get) if candidates else None

# Predict the next word for "python"
next_word = predict_next_word("python", conditional_probabilities)
print(f"\nPredicted next word after 'python': {next_word}")

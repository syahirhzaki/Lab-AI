# Q3(b) - Basic tweet preprocessing
import re


def preprocess_text(text):

    # Replace usernames with USER
    text = re.sub(r"@\w+", "USER", text)

    # Replace URLs with URL
    text = re.sub(r"https?://\S+", "URL", text)

    # Convert text to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


tweet = "@SkyAir My flight is NOT good! It was delayed again. https://airline.example"

clean_tweet = preprocess_text(tweet)

print(clean_tweet)

# Why "not" must stay: the Lab 8 CountVectorizer uses stop_words="english",
# and that list contains "not", so two opposite tweets end up with the same features.
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

print("\n'not' in scikit-learn's English stop words:", "not" in ENGLISH_STOP_WORDS)
v = CountVectorizer(stop_words="english")
X = v.fit_transform(["my flight is not good", "my flight is good"])
print("Vocabulary after stopword removal:", list(v.get_feature_names_out()))
print("Feature vector 'my flight is not good':", X.toarray()[0])
print("Feature vector 'my flight is good':    ", X.toarray()[1])

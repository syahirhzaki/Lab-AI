# Q1(c) - Rule-based classification of airline messages


def classify_message(tweet):
    tweet = tweet.lower()

    if "cancelled" in tweet or "delayed" in tweet:
        return "Service Complaint"

    elif "what time" in tweet or "departure" in tweet:
        return "Information Request"

    else:
        return "Other"


def should_prioritise(category):
    # Rule 2: a service complaint should be prioritised for support
    return category == "Service Complaint"


tweet_a = "My flight has been cancelled"
tweet_b = "What time does flight AB123 depart?"

print(classify_message(tweet_a))
print(classify_message(tweet_b))

# Extra: full tweets from part (a) and the priority rule
for name, tweet in [("A", "My flight has been cancelled and nobody has contacted me."),
                    ("B", "What time does flight AB123 depart?")]:
    category = classify_message(tweet)
    print(f"Tweet {name}: {category} | prioritise for support: {should_prioritise(category)}")

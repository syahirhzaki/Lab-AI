# Q4 - Why 80% accuracy is not enough: an example with 100 tweets
# 60 negative, 20 neutral, 20 positive. The model gets 80 right but misses most neutral tweets.
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

LABELS = ["negative", "neutral", "positive"]
y_true = ["negative"] * 60 + ["neutral"] * 20 + ["positive"] * 20
y_pred = (["negative"] * 60
          + ["neutral"] * 2 + ["negative"] * 18      # only 2 of 20 neutral tweets found
          + ["positive"] * 18 + ["negative"] * 2)

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Macro F1:", round(f1_score(y_true, y_pred, labels=LABELS, average="macro"), 3))
print("\nConfusion matrix (rows = true, columns = predicted):", LABELS)
print(confusion_matrix(y_true, y_pred, labels=LABELS))
print()
print(classification_report(y_true, y_pred, labels=LABELS, digits=3))

# Q2(b) - Semantic network as (subject, relation, object) triples

semantic_network = [
    ("Airline", "operates", "Flight"),
    ("Passenger", "books", "Flight"),
    ("Flight", "has", "Destination"),
    ("Flight", "has", "Departure Time"),
    ("Flight", "can be", "Delayed"),
    ("Flight", "can be", "Cancelled"),
    ("Delayed", "may cause", "Passenger Complaint"),
    # My own relationships
    ("Cancelled", "may cause", "Passenger Complaint"),
    ("Passenger", "makes", "Passenger Complaint"),
    ("Passenger Complaint", "is prioritised by", "Customer Support"),
]

for relationship in semantic_network:
    print(relationship)

# Simple query: what can a Flight be?
print("\nA Flight can be:", [o for s, r, o in semantic_network if s == "Flight" and r == "can be"])
# Simple query: what may cause a Passenger Complaint?
print("Causes of Passenger Complaint:", [s for s, r, o in semantic_network if r == "may cause" and o == "Passenger Complaint"])

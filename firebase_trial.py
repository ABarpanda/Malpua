import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Example: Add a document
# doc_ref = db.collection("locations").document("user_1")
# doc_ref.set({
#     "name": "Amritanshu",
#     "email": "amrit@example.com"
# })

# # Example: Read the document
# doc = doc_ref.get()
# print(doc.to_dict())

# Add document with custom ID
db.collection("users").document("user_123").set({
    "name": "Amritanshu",
    "email": "amrit@example.com",
    "age": 21
})

# OR add with auto-generated ID
doc_ref = db.collection("users").add({
    "name": "Riya",
    "email": "riya@example.com",
    "age": 22
})
print("Document created with ID:", doc_ref[1].id)

# Get specific document
doc = db.collection("users").document("user_123").get()
if doc.exists:
    print("Document data:", doc.to_dict())
else:
    print("No such document!")

# Get all documents
docs = db.collection("users").stream()
for d in docs:
    print(f"{d.id} => {d.to_dict()}")

# Update specific fields
db.collection("users").document("user_123").update({
    "age": 22,
    "email": "amrit.updated@example.com"
})

# Delete entire document
db.collection("users").document("user_123").delete()

# Delete a specific field from a document
# db.collection("users").document("user_456").update({
#     "age": firestore.DELETE_FIELD
# })

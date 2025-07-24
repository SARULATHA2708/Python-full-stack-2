from django.shortcuts import render, redirect
from pymongo import MongoClient
# MongoDB connection
client=MongoClient("mongodb+srv://lathachandra312:khe7GQ0mvZEKMEsv@cluster0.srnywrv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# client = MongoClient("mongodb+srv://sarudb:y5xrJnzngM3PvHRO@pythondbcluster.srgz3py.mongodb.net/")
db = client["mydb"]
collection = db["student"]
def index(request):
    students = list(collection.find())
    for s in students:
        s["id"] = str(s["_id"])
    return render(request, "index.html", {"students": students})
def add(request):
    if request.method == "POST":
        data = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "age": request.POST["age"],
            "phone": request.POST["phone"],
            "college": request.POST["college"],
            "department": request.POST["department"]
        }
        collection.insert_one(data)
        return redirect("index")
    return render(request, "add.html")
def edit(request, student_id):
    from bson.objectid import ObjectId
    student = collection.find_one({"_id": ObjectId(student_id)})
    if request.method == "POST":
        updated_data = {
            "name": request.POST["name"],
            "email": request.POST["email"],
            "age": request.POST["age"],
            "phone": request.POST["phone"],
            "college": request.POST["college"],
            "department": request.POST["department"]
        }
        collection.update_one({"_id": ObjectId(student_id)}, {"$set": updated_data})
        return redirect("index")
    return render(request, "edit.html", {"student": student, "student_id": student_id})

def delete(request, student_id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(student_id)})
    return redirect("index")

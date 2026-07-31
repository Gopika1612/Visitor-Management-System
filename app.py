from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
import json
DATA_FILE = "visitors.json"

def load_visitors():

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)

    with open(DATA_FILE, "r") as file:
        content = file.read().strip()

    if not content:
        return []

    return json.loads(content)


def save_visitors(visitors):

    with open(DATA_FILE, "w") as file:
        json.dump(visitors, file, indent=4)

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

# Create database tables

# Create uploads folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER PAGE ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        visitor_name = request.form["visitor_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        address = request.form["address"]
        employee_name = request.form["employee_name"]
        department = request.form["department"]
        purpose = request.form["purpose"]
        visit_date = request.form["visit_date"]
        visit_time = request.form["visit_time"]

        # Upload ID Proof
        id_file = request.files["id_proof"]

        filename = ""

        if id_file and id_file.filename != "":
            filename = secure_filename(id_file.filename)
            id_file.save(os.path.join("uploads", filename))

        visitors = load_visitors()

        visitor = {
            "visitor_id": len(visitors) + 1,
            "visitor_name": visitor_name,
            "email": email,
            "phone": phone,
            "gender": gender,
            "address": address,
            "employee_name": employee_name,
            "department": department,
            "purpose": purpose,
            "visit_date": visit_date,
            "visit_time": visit_time,
            "id_proof": filename,
            "status": "Pending"
        }

        visitors.append(visitor)

        save_visitors(visitors)

        return redirect("/success")

    return render_template("visitor_register.html")


# ---------------- EMPLOYEE PAGE ----------------
@app.route("/employee")
def employee():

    search = request.args.get("search", "")

    visitors = load_visitors()

    if search:
        visitors = [
            visitor for visitor in visitors
            if search.lower() in visitor["visitor_name"].lower()
        ]

    return render_template(
        "employee_approval.html",
        visitors=visitors,
        search=search
    )

@app.route("/approve/<int:visitor_id>")
def approve(visitor_id):

    visitors = load_visitors()

    for visitor in visitors:
        if visitor["visitor_id"] == visitor_id:
            visitor["status"] = "Approved"
            break

    save_visitors(visitors)

    return redirect("/employee")
@app.route("/reject/<int:visitor_id>")
def reject(visitor_id):

    visitors = load_visitors()

    for visitor in visitors:
        if visitor["visitor_id"] == visitor_id:
            visitor["status"] = "Rejected"
            break

    save_visitors(visitors)

    return redirect("/employee")

# ---------------- REPORTS ----------------
@app.route("/reports")
def reports():

    visitors = load_visitors()

    return render_template(

        "reports.html",
        visitors=visitors
    )


# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- SUCCESS ----------------
@app.route("/success")
def success():
    return render_template("success.html")
@app.route("/visitor_pass")
def visitor_pass():
    visitors = load_visitors()
    return render_template("visitor_pass.html", visitors=visitors)
# ---------------- CHECK-IN / CHECK-OUT ----------------
@app.route("/checkin")
def checkin():

    visitors = load_visitors()

    return render_template(
        "checkin.html",
        visitors=visitors
    )

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect,request,session,url_for,abort,flash
from admin.second import second
from flask_sqlalchemy import SQLAlchemy

codeset = "yuvraaj"

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register blueprint
app.register_blueprint(second, url_prefix="/admin")

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    amt = db.Column(db.Integer, default=10)
    psswd =db.Column(db.String(100), nullable=False)
    fdamt=db.Column(db.Integer, default=0)

# Create the database
with app.app_context():
    db.create_all()

    # ✅ Only add master user if it doesn't already exist
    master_exists = User.query.get(99)
    if not master_exists:
        master = User(id=99, name="yuvraaj_main", amt=100, psswd="yuvraaj_password")
        db.session.add(master)
        db.session.commit()




@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            return "❌ Username already taken.", 400
        
        new_u = User(name=username, psswd=password)
        db.session.add(new_u)
        db.session.commit()
        
        # ====== Highlighted change: log user in by setting session here ======
        session["user_id"] = new_u.id
        session["username"] = new_u.name
        session["amt"]= new_u.amt
        
        return redirect(url_for("acc",id=new_u.id))
    return render_template("signup.html")





@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # ✅ MASTER LOGIN CHECK
        if username == "yuvraaj_main" and password == "yuvraaj_password":
            session["user_id"] = 99  # ✅ Real DB ID
            session["username"] = "yuvraaj_main"
            session["is_master"] = True

        # ✅ Normal DB login
        user = User.query.filter_by(name=username, psswd=password).first()

        if user:
            session["user_id"] = user.id
            session["username"] = user.name
            session["is_master"] = False
            return redirect(url_for("acc"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/acc")
def acc():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # ✅ MASTER ACCOUNT VIEW
    if session.get("is_master"):
        master_user = {
            "id": 99,
            "name": "yuvraaj_main",
            "amt": 100,
            "psswd": "yuvraaj_password"
        }
        return render_template("acc.html", user=master_user)

    # ✅ NORMAL DB USER VIEW
    user_id = session["user_id"]
    user = User.query.get(user_id)

    if not user:
        return "No such user"

    return render_template("acc.html", user=user)


@app.route("/clear_users")
def clear_users():
    User.query.filter(User.id != 99).delete()   # ✅ keep master
    db.session.commit()
    return "All users (except Master) deleted!"





@app.route("/admin/setcode", methods=["GET", "POST"])
def setcode():
    codeset = "yuvraaj"
    users = None

    if request.method == "POST":
        code = request.form.get("code")

        if code == codeset:
            users = User.query.all()
        else:
            flash("Invalid admin code!", "error")

    # ✅ Make sure admin_page.html exists
    return render_template("setcode.html", users=users)





@app.route("/sendfunds", methods=["GET", "POST"])
def send():
    sender_id = session.get("user_id")
    if not sender_id:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        rec_id = request.form.get("receiver_id")  # ✅ fixed spelling
        amount = int(request.form.get("amount"))

        # ✅ check if rec_id is empty
        if not rec_id:
            return "❌ No receiver ID entered"

        # ✅ cast to int before querying
        receiver = User.query.get(int(rec_id))  

        sender = User.query.get(sender_id)

        if receiver is None:
            return "❌ Receiver does not exist"

        if amount <= 0:
            return "❌ Invalid amount"

        if sender.amt < amount:
            return "❌ Not enough funds"

        sender.amt -= amount
        receiver.amt += amount
        db.session.commit()

        return f"✅ Sent {amount} to {receiver.name} (ID {receiver.id})"

    return render_template("send.html")

@app.route("/fixed_deposit", methods=["GET", "POST"])
def fixed_deposit():
    sender_id = session.get("user_id")
    if not sender_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            amount = int(request.form.get("amount"))
            duration = request.form.get("duration")
        except (ValueError, TypeError):
            return "❌ Invalid input"

        if amount <= 0:
            return "❌ Invalid amount entered"

        sender = User.query.get(sender_id)
        bank = User.query.get(99)

        if not bank:
            return "❌ FD Bank Account (ID 99) does not exist!"

        if sender.amt < amount:
            return "❌ Not enough funds in your account"

        # ✅ Transfer to fixed deposit
        sender.amt -= amount
        sender.fdamt += amount
        bank.amt += amount
        db.session.commit()

        return f"✅ Fixed Deposit of {amount} created for {duration} years. Funds transferred to FD account!"

    return render_template("fixed_deposit.html")

   




@app.route("/finduser", methods=["GET", "POST"])
def find_user():
    if request.method == "POST":
        rec_id = request.form.get("receiver_id")

        # ✅ Check if ID was provided and convert to int
        if not rec_id:
            return "❌ Please enter a Receiver ID"

        receiver = User.query.get(int(rec_id))

        if receiver:
            return f"✅ User found: {receiver.name} (ID {receiver.id})"
        else:
            return "❌ User not found"

    return render_template("finduser.html")





    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("home")



if __name__ == "__main__":
    app.run(debug=True)


from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from helpers import error, login_required
from tempfile import mkdtemp

app = Flask(__name__)

db = SQL("sqlite:///piratehub.db")

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    piratehubdata = db.execute("SELECT DISTINCT dataname, type, price FROM piratedata")
    return render_template("index.html",piratehubdatatable=piratehubdata)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/service")
def service():
    return render_template("service.html")

@app.route("/admin",methods=["GET","POST"])
@login_required
def admin():
    if request.method == "POST":
        owneradminid = request.form.get("adminid")
        piratedataname = request.form.get("dataname")
        piratedatatype = request.form.get("type")
        piratedataprice = request.form.get("price")
        piratedatasize = request.form.get("size")
        # print("adminid="+str(owneradminid))
        if not piratedataname or not piratedatatype:
            return error()
        checkpiratedata = db.execute("SELECT * FROM piratedata WHERE dataname=? AND adminid=?",piratedataname,owneradminid)
        if not checkpiratedata:
            db.execute("INSERT INTO piratedata(adminid,dataname,type,price,size) VALUES(?,?,?,?,?)",owneradminid,piratedataname,piratedatatype,piratedataprice,piratedatasize)
        return redirect("/")
    else:
        adminloginstatus = request.args.get("adminlogin")
        if not session.get("admin_id") is None:
            adminloginstatus = "success"
        admindata = db.execute("SELECT * FROM admins WHERE id=?",session["admin_id"])
        return render_template("admin.html",adminlogincheck=adminloginstatus,adminname=admindata[0]["adminname"],adminid=admindata[0]["id"])
        
@app.route("/login",methods=["GET","POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("adminname"):
            return error()
        if not request.form.get("password"):
            return error()
        admindata = db.execute("SELECT * FROM admins WHERE adminname=?",request.form.get("adminname"))
        if len(admindata) != 1 or not admindata[0]["password"] == request.form.get("password"):
            return error()
        session["admin_id"] = admindata[0]["id"]
        return redirect("/admin?adminlogin=success")  
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

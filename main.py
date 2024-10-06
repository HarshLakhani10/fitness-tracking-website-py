from flask import Flask,url_for,render_template,redirect,request,session,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "myfitnessproject"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "fitness"  

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("fname")
        passw = request.form.get("password")
        # for storing name of the logged in user in variable to use it later
        global user_name
        user_name = request.form.get("fname")
        print(user_name)
        cur = mysql.connection.cursor()
        cur.execute(f"""select username,password from user where username=%s and password=%s""",(name,passw))
        userr = cur.fetchone()
        print(name)
        cur.execute(f"""select id from user where username=\"{name}\"""")
        global UserrId 
        UserrId = cur.fetchone()
        UserrId = UserrId[0]
        cur.close()
        if userr is None:
            return render_template("pass.html",n = name,p = passw,error = "invalid username or password")
        elif name == userr[0] and passw == userr[1]:
            # storing user in session
            session["user"] = userr
            flash("you are successfully logged in.")
            return render_template("index.html")
        else:
            return render_template("pass.html",n = name,p = passw,error = "you have done something horrible")
    else:
        return render_template("login.html")
    
@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("fname")
        passw = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO user (username,password) VALUES (%s,%s)""",(name,passw))
        mysql.connection.commit()
        cur.close()
        return render_template("pass.html",n = name,p = passw)
    else:
        return render_template("Register.html")

@app.route("/menu")
def menu():
    if "user" in session:
        return render_template("menu.html")
    else:
        return redirect(url_for("login"))
    
# for giving dynamic content in dataentry.html page
    
def paragraphs(index):
    excerciseDiscription = [
        "Push-ups are a foundational bodyweight exercise that targets the chest, shoulders, and triceps while also engaging the core muscles for stability. They can be modified to suit various fitness levels and goals, making them a versatile addition to any workout routine.",
        "The chest press, whether performed with dumbbells, a barbell, or a machine, primarily targets the pectoral muscles (chest). It's effective for building upper body strength and muscle mass, and variations like incline and decline presses help target different areas of the chest.",
        "Chest flies isolate the chest muscles and are excellent for developing muscle definition and strength. By performing the movement in a controlled manner, you can effectively target the chest while minimizing stress on the shoulders.",
        "Barbell curls are a classic biceps exercise that targets the front of the upper arm. They're effective for building size and strength in the biceps and can be varied by changing grip width or using an EZ-curl bar.",
        "Biceps curls with dumbbells allow for a greater range of motion and unilateral training, helping to address strength imbalances between the arms. By focusing on a full range of motion and controlling the weight, you can maximize muscle engagement and growth.",
        "Preacher curls isolate the biceps by eliminating momentum and stabilizing the upper arms. This seated or standing exercise is excellent for targeting the peak of the biceps and developing overall arm strength.",
        "Deadlifts are a compound exercise that targets multiple muscle groups, including the hamstrings, glutes, lower back, and grip strength. They're essential for building functional strength and power and can be adapted for various fitness levels with different equipment.",
        "Pull-ups are a challenging bodyweight exercise that primarily targets the back muscles, including the latissimus dorsi and rhomboids, as well as the biceps. They're excellent for building upper body strength and improving grip strength and can be modified with different grip widths.",
        "Seated rows target the muscles of the upper back, including the rhomboids, traps, and rear deltoids. By retracting the shoulder blades and pulling the handle towards the torso, you can effectively strengthen and sculpt the back muscles.",
        "Dips primarily target the triceps, chest, and shoulders and are excellent for building upper body strength and muscle mass. By adjusting body position and hand placement, you can emphasize different muscle groups and increase or decrease resistance.",
        "Tricep rope pushdowns isolate the triceps and are effective for building muscle definition and strength in the back of the arms. By maintaining tension throughout the movement and focusing on the contraction at the bottom, you can maximize triceps activation.",
        "Triceps kickbacks target the triceps and are excellent for developing muscle definition and strength in the back of the arms. By keeping the upper arm stationary and extending the forearm backward, you can effectively isolate the triceps.",
        "Shoulder presses target the deltoid muscles of the shoulders and are essential for building upper body strength and muscle mass. By using dumbbells or a barbell and maintaining proper form, you can effectively target the shoulders while minimizing stress on the joints.",
        "Behind-the-back shoulder presses target the rear deltoids and are excellent for developing overall shoulder strength and stability. By using proper form and controlling the weight, you can effectively target the muscles of the shoulders and upper back.",
        "Shoulder press machines provide stability and support, making them suitable for beginners or those with joint issues. By adjusting the seat and hand positions, you can target different areas of the shoulders and upper body.",
        "Squats are a compound exercise that targets the quadriceps, hamstrings, glutes, and core muscles. They're essential for building lower body strength and power and can be performed with bodyweight or additional resistance.",
        "Sumo squats target the inner thigh muscles (adductors) and are excellent for building lower body strength and muscle mass. By using a wide stance and keeping the knees aligned with the toes, you can effectively target the muscles of the inner thighs.",
        "Lunges are a unilateral exercise that targets the quadriceps, hamstrings, glutes, and core muscles. They're excellent for improving balance, stability, and coordination and can be performed with bodyweight or additional resistance."
    ]
    return excerciseDiscription[index]

# for giving dynamic content in dataentry.html page

def imagePaths(index):
    image_paths = [
        "images/push-up.jpg",
        "images/chest-press.jpg",
        "images/chest-fly.jpg",
        "images/barbell-curl.jpg",
        "images/biceps-curl.jpg",
        "images/preacher-curl.jpg",
        "images/deadlift.jpg",
        "images/pull-ups.jpg",
        "images/seated-row.jpg",
        "images/dips.jpg",
        "images/tricep-rope-pushdown.jpg",
        "images/triceps-kickback.jpg",
        "images/shoulderpress.jpg",
        "images/behindback-shouolder-press.jpg",
        "images/shoulder-press-machine.jpg",
        "images/squat.jpg",
        "images/sumo-squat.jpg",
        "images/lunges.jpg"
    ]
    return image_paths[index]

# for giving database entry for perticular excersice

def ex_name_database(index):
    ex_database = [
        "chest1",
        "chest2",
        "chest3",
        "biceps1",
        "biceps2",
        "biceps3",
        "back1",
        "back2",
        "back3",
        "triceps1",
        "triceps2",
        "triceps3",
        "shoulder1",
        "shoulder2",
        "shoulder3",
        "legs1",
        "legs2",
        "legs3",
    ]
    return ex_database[index]

@app.route("/dataentry/<heading>/<int:indexno>")
def display(heading,indexno):
    global headingv
    headingv = heading
    global img_path 
    img_path = imagePaths(indexno)
    global indexnov
    indexnov = paragraphs(indexno)
    global ex_databse_value
    ex_databse_value = ex_name_database(indexno)
    print(ex_databse_value)
    print(user_name)
    return render_template("dataentry.html",heading=headingv,desc=indexnov,image=img_path)

@app.route("/xyz",methods = ["GET","POST"])
def dataentry():
    if request.method == "POST":
        date = request.form.get("cDate")
        weight = request.form.get("weight")
        excersice = ex_databse_value
        cur = mysql.connection.cursor()
        cur.execute(f"""INSERT INTO userdata (user,exdate,{excersice}) VALUES (%s,%s,%s)""",(user_name,date,weight))
        mysql.connection.commit()
        cur.close()
        return render_template("dataentry.html",heading=headingv,desc=indexnov,image=img_path)
    else:
        return render_template("dataentry.html",heading=headingv,desc=indexnov,image=img_path)

@app.route("/logout")
def logout():
    session.pop('user',None)
    return render_template("index.html")

@app.route("/profile")
def profile():
    if "user" in session:
        print(user_name)
        try:
            if EditName == None:
                pass
        except:
            return render_template("profile.html",user_name = user_name,UserAge="xx",UserEmail="xxxxxxxxxxxxxx") 
        else:
            return render_template("profile.html",user_name = EditName,UserAge=EditAge,UserEmail=EditEmail)
    else:
        return redirect(url_for("login"))

@app.route("/editprofile",methods = ["GET","POST"])
def editprofile():
    if "user" in session:
        if request.method == "POST":
            UsernameE = request.form.get("Usernamef")
            AgeE = request.form.get("agef")
            EmailE = request.form.get("emailf")
            cur = mysql.connection.cursor()
            cur.execute(f"""update user set displayname=\"{UsernameE}\",age=\"{AgeE}\",email=\"{EmailE}\" where id={UserrId}""")
            mysql.connection.commit()
            cur.close()
            global EditName
            EditName = UsernameE
            global EditAge
            EditAge = AgeE
            global EditEmail
            EditEmail = EmailE
            print(EditName)
            print(EditAge)
            print(EditEmail)
            print(UserrId)
            return render_template("profile.html",user_name = EditName,UserAge=EditAge,UserEmail=EditEmail)
        else:
            return render_template("editprofile.html")
    else:
        return redirect(url_for("profile"))

@app.route("/progress")
def progress():
    if "user" in session:
        # print(user_name)
        ProgressExcercise = ex_databse_value
        # print(ProgressExcercise)
        cur = mysql.connection.cursor()
        cur.execute(f"""SELECT exdate,{ProgressExcercise} FROM userdata where user=\"{user_name}\"""")
        ProgressData = cur.fetchall()
        # print(ProgressData)
        mysql.connection.commit()
        cur.close()
        ProgressDataDate = []
        ProgressDataWeight = []
        for Data in ProgressData:
            ProgressDataDate.append(Data[0])
            ProgressDataWeight.append(Data[1])
        TempList = []
        for i in range(len(ProgressDataWeight)):
            if ProgressDataWeight[i] == 0:
                TempList.append(i)
            else:
                continue
        print(TempList)
        print(ProgressDataDate)
        print(ProgressDataWeight)
        ProgressDataDate = [value for index, value in enumerate(ProgressDataDate) if index not in TempList]
        ProgressDataWeight = [value for index, value in enumerate(ProgressDataWeight) if index not in TempList]
        print(TempList)
        print(ProgressDataDate)
        print(ProgressDataWeight)

        labels = ProgressDataDate
 
        data = ProgressDataWeight
        # Return the components to the HTML template 
        return render_template(
            template_name_or_list='progress.html',
            data=data,
            labels=labels,
    )
        # return render_template("progress.html")
    else:
        return redirect(url_for("login"))
        
   

#!c:\\UsersFethi\\AppData\\Local\\Microsoft\\WindowsApps\\python
from flask import Flask, render_template, request, jsonify
import pandas as pd
import mysql.connector as mariadb
import pandas as pd
import cv2
from base64 import b64encode
import numpy as np
from mnist_predict import predict_img
import PIL.Image as Image
from pathlib import Path
import json

#déclaration des variables des dossiers de modèle et de l'image
CUR_DIR = Path.cwd()
DATA_DIR = CUR_DIR/"data"
FIC_MODEL = DATA_DIR/"model_knn.pkl"
IMG_DIR = CUR_DIR/"images"
IMG_FIC = IMG_DIR/"output_img.png"
app = Flask(__name__)

#######################################################
#                   affichage la page index           #
#######################################################
@app.route("/")
def index():
    return render_template("index.html")

######################################################
#                    Question n:1                    #
######################################################

@app.route("/hello")
def hello():
    return "Hello world!"


######################################################
#                   Question n:2                     #
######################################################

@app.route("/hello_style")
def style():
    return render_template("index.html", rep = "Binevenue dans mon site pour explorer le frameworke flask")

######################################################
#               Question n:3                         #
# ####################################################
@app.route("/home")
def home():
    return render_template("home.html", message_home="vous allez être dériger vers une autre page cliquez sur le lien")

@app.route("/suivant")
def redirect():
    return render_template("redirect_page.html") 


######################################################
#                   Question n:4  Formulaire         #
######################################################
@app.route("/formulaire")
def Formulaire():
    return render_template("Formulaire.html")

@app.route("/post_formulaire", methods=["get","POST"])
def formul():
    if request.method == "POST":
        civil = "Monsieur" if request.form["civil"] == "Mr" else "Madame"
        user_name = request.form["user_name"].upper()
        prenom = request.form["prenom"].capitalize()
        user_mail = request.form["user_mail"]
        return render_template("confirmation.html", confirmation=f"Bienvenue {civil} {prenom} {user_name}, votre adresse e_mail est: {user_mail}")
    else: 
        return render_template("confirmation.html",message = "la page à été actualisée")


############################################################
#                       Question n: 5 base de données      #
############################################################



@app.route('/crud')
def crud():
    return render_template("connexion.html")

@app.route('/posted', methods=["POST"])
def create():
   
    try:
        # Connexion au SGBDR MariaDB
        db = mariadb.connect(host='localhost', user='root', password='')
        # Instanciation d'un curseur
        curseur = db.cursor()
        # Requetage SQL 
        curseur.execute("CREATE DATABASE IF NOT EXISTS users")
        curseur.execute("USE users")
        curseur.execute("CREATE TABLE IF NOT EXISTS user_info (user_id int not null auto_increment ,nom VARCHAR(255) not null," +
                       "prenom VARCHAR(255) not null, sexe enum('Masculin','Feminin') not null, psudo varchar(255) unique, primary key (`user_id`))")
        #recupération les information des champs input & select
        sexe = request.form["sexe"] 
        fName = request.form["fName"].capitalize()
        lName = request.form["lName"].upper()
        psudo = request.form["psudo"]
        print(sexe)
        curseur.execute(f"INSERT INTO user_info (Nom,Prenom,sexe,Psudo) VALUES ('{lName}','{fName}','{sexe}','{psudo}' )")
        db.commit()
        curseur.close()
        db.close()
        return render_template("connexion.html" , succes =  f"Les données sont inseré avec succès")
    except mariadb.Error as e:
        return render_template("connexion.html", erreur = f"Erreur insertion: {e}")

#6. Faire une page /utilisateurs-inscrits qui permet de lister tous 
# les noms d'utilisateurs présents dans la base de donnée.

@app.route("/list_users", methods=["POST"])
def select():
    # Connexion au SGBDR MariaDB
    try:
        columns = ["Nom","Prenom","sexe","Psudo"]
        db="users"
        connect = mariadb.connect(host='localhost', user='root', password='', database=db)
        curseur = connect.cursor()
        curseur.execute("select Nom,Prenom,sexe,Psudo from user_info ")
        result = curseur.fetchall()
        return render_template("list_users.html" , data =  result,col = columns)
    except Exception as error:
        return render_template("connexion.html", erreur = f"Erreur insertion: {error}")

############################################################################
#                         question n:6                                     #
############################################################################
@app.route("/export")
def export():
    return render_template("export_dataframe.html")



@app.route("/show_csv_statistique", methods=["GET", "POST"])
def show_csv():
    if request.method == 'POST':
        csv = request.files.get('fichier')
        sep = request.form.get('delimiter')
        df = pd.read_csv(csv,delimiter=sep)
        table1 = df.describe()
        table1.insert(0,"Index",table1.index, allow_duplicates=False)
        table2 = df.corr()
        table2.insert(0,"Index",table2.index, allow_duplicates=False)
        return render_template("export_dataframe.html", rest="ok",describe_col = table1.columns, 
                                                        describe_values=table1.values, 
                                                        corr_col = table2.columns, coor_values=table2.values)


###################################################################################################################
#                                   Question 8: mnist                                                             #
###################################################################################################################

@app.route("/predict", methods=["GET","POST"])  
def predict():
    if request.method == "POST":
        file = request.files.get('imageFile')
        base64img = "data:image/png;base64,"+b64encode(file.getvalue()).decode('ascii')
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        prediction = predict_img(img)
        num = int(prediction)
        print(num)
        return render_template("load_image.html", prediction =num, image =base64img  )
    else:
        return render_template("load_image.html")

if __name__ == '__main__':
    app.run(debug=True)


import random

from flask import Flask, jsonify
from flask import request
from flask import render_template_string,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import  Mapped,mapped_column
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import sessionmaker
from flask import session, redirect, url_for, flash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)
app.secret_key = 'f53a8c34a0e84bfae4393ffaf7be4ad7cfc2c7fba4ec5d4fa17a43a6c12c71c4'  # або будь-який інший випадковий рядок



class User(db.Model):
    __tablename__ = 'users_poczta'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(128), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(128), nullable=False)
    role: Mapped[str] = mapped_column(db.String(20), default='user')  # 'user' або 'admin'


def set_password(self, password):
    self.password_hash = generate_password_hash(password)


def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Package(db.Model):
    __tablename__= 'package'
    id: Mapped[int] = mapped_column(db.Integer,primary_key= True)
    name_package : Mapped[str] = mapped_column(db.String(128),nullable=False)
    content :Mapped[str] = mapped_column(db.String(128),nullable=False)
    departure_city: Mapped[str] = mapped_column(db.String(128),nullable=False)
    arrival_city :Mapped[str] = mapped_column(db.String(128),nullable=False)
    status_package : Mapped[str] = mapped_column(db.String(128),nullable=False)
CITY_CODES = {
    "Днепр": 1,
    "Черкассы": 2,
    "Одесса": 3,
    "Киев": 4,
    "Харьков": 5,
    "Львов": 6,
    "Запорожье": 7,
    "Ивано-Франковск": 8,
    "Полтава": 9,
    "Тернополь": 10,
    "Ужгород": 11,
    "Чернигов": 12,
    "Черновцы": 13,
    "Винница": 14,
    "Херсон": 15,
    "Николаев": 16,
    "Сумы": 17,
    "Житомир": 18,
    "Кривой Рог": 19,
    "Мариуполь": 20,
    "Луганск": 21,
    "Донецк": 22,
    "Краматорск": 23,
    "Славянск": 24,
    "Хмельницкий": 25,
    "Луцк": 26,
    "Ровно": 27,
    "Бровары": 28,
    "Белая Церковь": 29,
    "Кременчуг": 30,
    "Мелитополь": 31,
    "Павлоград": 32,
    "Бердянск": 33,
    "Конотоп": 34,
    "Умань": 35,
    "Нежин": 36,
    "Мукачево": 37,
    "Каменское": 38,
    "Александрия": 39,
    "Северодонецк": 40,
    "Кропивницкий": 41
}


with app.app_context():
    db.create_all()


def show_add_package():
    return render_template('add_package.html')


def do_the_add_package():
    name_package = request.form.get('name_package')
    content = request.form.get('content')
    arrival_city= request.form.get('arrival_city')
    dep_city = request.form.get('dep_city')
    status = request.form.get('status')
    all_info_package = name_package,dep_city,status,content,arrival_city

    new_package =Package(
        name_package = "BR321",
        content=request.form.get('content'),
        arrival_city=request.form.get('arrival_city'),
        departure_city = request.form.get('dep_city'),
        status_package = request.form.get('status')

    )
    db.session.add(new_package)
    db.session.commit()

    new_package.name_package = f"Посылка №{new_package.id}"

    db.session.commit()

    city_code = CITY_CODES.get(dep_city, 0)  # если города нет в словаре — 0
    arrival_city_code= CITY_CODES.get(arrival_city,0)
    new_package.name_package = f"Посылка №{new_package.id}-{city_code}-{arrival_city_code}"

    db.session.commit()


    return render_template("sucses.html")


@app.route("/add_package",methods=['POST','GET'])
def add_package():
    if request.method == "POST":
        return do_the_add_package()
    else:
        return show_add_package()



@app.route('/packages', methods=['GET'])
def get_packages():

    packages = Package.query.all()


    result = [
        {"id": package.id,
         "name_package": package.name_package,
         "departure_city": package.departure_city,
         "status_package": package.status_package
         }
        for package in packages
    ]

    return jsonify(result)



@app.route('/a/<int:package_id>', methods=['PUT'])
def update_status(package_id):
    data = request.json
    new_status = data.get('status_package')

    if not new_status:
        return jsonify({"error": "Новый статус обязателен"}), 400

    package = Package.query.get(package_id)

    if package:
        package.status_package = new_status
        db.session.commit()
        return jsonify({"message": "Статус обновлён"}), 200
    else:
        return jsonify({"error": "Посылка не найдена"}), 404

@app.route("/update_package", methods=["GET"])
def show_update_package():
    packages = Package.query.all()
    return render_template("update_package.html",packages=packages)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            return "Пользовател уже существует"

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role

            if user.role == "admin":
                return redirect(url_for("package_manager"))
            else:
                return redirect(url_for("user_dashboard"))

        return "Неверный логин или пароль"

    return render_template("login.html")

@app.route("/dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("user_dashboard.html")


@app.route('/package_manager')
def package_manager():
    if session.get("role") != "admin":
        flash("Доступ заборонено")
        return redirect(url_for("login"))
    return render_template("main.html")
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
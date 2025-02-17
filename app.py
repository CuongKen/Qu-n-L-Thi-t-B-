from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///computers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/images"
app.secret_key = "supersecretkey"

db = SQLAlchemy(app)

# Đảm bảo thư mục lưu ảnh tồn tại
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Định nghĩa Model
class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100), nullable=False)
    specifications = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=True)

# Trang Home
@app.route("/")
def home():
    return render_template("home.html")

# Trang danh sách thiết bị có chức năng tìm kiếm
@app.route("/devices", methods=["GET", "POST"])
def index():
    search_query = request.form.get("search", "").strip()
    
    if search_query:
        computers = Computer.query.filter(
            (Computer.device_name.contains(search_query)) |
            (Computer.brand.contains(search_query)) |
            (Computer.location.contains(search_query)) |
            (Computer.status.contains(search_query))
        ).all()
    else:
        computers = Computer.query.all()

    return render_template("index.html", computers=computers, search_query=search_query)

# Thêm thiết bị
@app.route("/add", methods=["GET", "POST"])
def add_computer():
    if request.method == "POST":
        device_name = request.form.get("device_name")
        specifications = request.form.get("specifications")
        brand = request.form.get("brand")
        location = request.form.get("location")
        status = request.form.get("status")

        # Xử lý ảnh tải lên
        image_file = request.files.get("image")
        image_path = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)
            image_path = image_path.replace("\\", "/")

        new_computer = Computer(
            device_name=device_name,
            specifications=specifications,
            brand=brand,
            location=location,
            status=status,
            image=image_path
        )
        db.session.add(new_computer)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("add.html")

# Sửa thiết bị
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_computer(id):
    computer = Computer.query.get_or_404(id)

    if request.method == "POST":
        computer.device_name = request.form.get("device_name", computer.device_name)
        computer.specifications = request.form.get("specifications", computer.specifications)
        computer.brand = request.form.get("brand", computer.brand)
        computer.location = request.form.get("location", computer.location)
        computer.status = request.form.get("status", computer.status)

        # Xử lý ảnh mới nếu có
        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)
            computer.image = image_path.replace("\\", "/")

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("edit.html", computer=computer)

# Xóa thiết bị
@app.route("/delete/<int:id>")
def delete_computer(id):
    computer = Computer.query.get_or_404(id)
    db.session.delete(computer)
    db.session.commit()
    return redirect(url_for("index"))

# Tạo database nếu chưa có
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

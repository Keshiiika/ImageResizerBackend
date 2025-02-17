import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import tweepy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Twitter API Authentication
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
api = tweepy.API(auth)

# Image Sizes
SIZES = [(300, 250), (728, 90), (160, 600), (300, 600)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path):
    img = Image.open(image_path)
    resized_images = []
    for size in SIZES:
        img_resized = img.resize(size)
        new_path = os.path.join(UPLOAD_FOLDER, f"resized_{size[0]}x{size[1]}.jpg")
        img_resized.save(new_path)
        resized_images.append(new_path)
    return resized_images

# def post_to_x(image_paths):
#     media_ids = []
    
#     for image in image_paths:
#         # Upload media using API v2
#         media = api.media_upload(image)
#         media_ids.append(media.media_id_string)  # Store media ID
    
#     # Post tweet with media
#     api.update_status(status="Here are your resized images!", media_ids=media_ids)
def post_to_x(image_paths):
    for image in image_paths:
        print(f"Image processed and saved at: {image}")  # Simulating saving instead of posting


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            return "Invalid file type"
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Ensure folder exists before saving
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        file.save(filename)

        # Resize & Post
        resized_images = resize_image(filename)
        post_to_x(resized_images)

        return redirect(url_for("uploaded_file", filename=file.filename))
    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)

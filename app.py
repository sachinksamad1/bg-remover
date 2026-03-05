import os
import io
from flask import Flask, request, render_template, send_file, jsonify
from rembg import remove, new_session
from PIL import Image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

# Point rembg to the bundled model directory
os.environ["U2NET_HOME"] = os.path.join(os.path.dirname(__file__), "models")

# Rembg expects the bria-rmbg model to be named exactly "bria-rmbg.onnx"
model_dir = os.environ["U2NET_HOME"]
bria_original = os.path.join(model_dir, "bria-rmbg-2.0.onnx")
bria_expected = os.path.join(model_dir, "bria-rmbg.onnx")

if os.path.exists(bria_original) and not os.path.exists(bria_expected):
    os.rename(bria_original, bria_expected)

# Initialize the model session once at startup
try:
    session = new_session("bria-rmbg")
except Exception as e:
    print(f"Warning: Failed to initialize bria-rmbg session: {e}")
    session = None


def allowed_file(filename):
    """Check if the uploaded file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Serve the main upload page."""
    return render_template("index.html")


@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    """Accept an image upload, remove its background, and return the result."""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type. Please upload a PNG, JPG, JPEG, WEBP, or BMP image."}), 400

    try:
        img = Image.open(file.stream)
        
        # Pass the pre-loaded session to avoid loading the model on every request
        if session:
            output = remove(img, session=session)
        else:
            output = remove(img)

        img_io = io.BytesIO()
        output.save(img_io, "PNG")
        img_io.seek(0)

        # Build a download filename from the original
        original_name = os.path.splitext(file.filename)[0]
        download_name = f"{original_name}_no_bg.png"

        return send_file(
            img_io,
            mimetype="image/png",
            as_attachment=False,
            download_name=download_name,
        )

    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500


@app.route("/health")
def health():
    """Health check endpoint for Cloud Run."""
    return jsonify({"status": "healthy"}), 200


@app.errorhandler(413)
def too_large(e):
    """Handle file-too-large errors."""
    return jsonify({"error": "File is too large. Maximum size is 16 MB."}), 413


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
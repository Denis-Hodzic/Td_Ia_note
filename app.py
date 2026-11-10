"""Flask app: display the Quadtree of Velonecy bike stations for a chosen capacity."""
from flask import Flask, render_template, request

from quadtree_utils import generate_plot

app = Flask(__name__)

CAPACITY_MIN, CAPACITY_MAX, CAPACITY_DEFAULT = 1, 100, 8


def parse_capacity(raw):
    """Validate the `capacity` query parameter. Returns (value, error_message)."""
    if raw is None or raw == "":
        return CAPACITY_DEFAULT, None
    try:
        value = int(raw)
    except ValueError:
        return None, "Capacity must be an integer."
    if not CAPACITY_MIN <= value <= CAPACITY_MAX:
        return None, f"Capacity must be between {CAPACITY_MIN} and {CAPACITY_MAX}."
    return value, None


@app.route("/", methods=["GET"])
def index():
    capacity, error = parse_capacity(request.args.get("capacity"))
    if error:
        # 400 Bad Request: invalid user input, page still rendered with the message
        return render_template("index.html", error=error,
                               capacity=request.args.get("capacity"),
                               cmin=CAPACITY_MIN, cmax=CAPACITY_MAX), 400

    image, n_nodes = generate_plot(capacity)
    return render_template("index.html", image=image, n_nodes=n_nodes,
                           capacity=capacity, cmin=CAPACITY_MIN, cmax=CAPACITY_MAX)


if __name__ == "__main__":
    # 0.0.0.0 so the app is reachable from outside the Docker container
    app.run(host="0.0.0.0", port=5000)

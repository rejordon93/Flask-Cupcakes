from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


app = Flask(__name__)

# ... Your other code ...


@app.route('/')
def index():
    """Render the index page"""

    return render_template('index.html')


def serialize_cupcake(cupcake):
    """Serialize a Cupcake model instance to a dictionary."""
    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }


@app.route('/api/cupcakes')
def list_all_cupcakes():
    """Return Json {cupcakes: [{id, flavor, size, rating, image}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.route("/cupcakes/<cupcake_id>")
def list_single_cupcake(cupcake_id):
    """Return JSON {'cupcake': {id, name, calories}}"""

    cupcake = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/cupcakes", methods=["POST"])
def create_cupcake():
    """Create cupcakes from form data & return it.

    Returns JSON {'cupcake': {id, flavor, size, rating, image}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=serialized), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake with the provided id in the URL and flavor, size, rating, and image data from the request body.
    Returns JSON {'cupcake': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get(cupcake_id)
    if not cupcake:
        return jsonify(error='Cupcake not found'), 404

    flavor = request.json.get("flavor", cupcake.flavor)
    size = request.json.get("size", cupcake.size)
    rating = request.json.get("rating", cupcake.rating)
    image = request.json.get("image", cupcake.image)

    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = rating
    cupcake.image = image

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake with the provided id in the URL.
    Returns JSON {'message': 'Deleted'}"""

    cupcake = Cupcake.query.get(cupcake_id)
    if not cupcake:
        return jsonify(error='Cupcake not found'), 404

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='Deleted')

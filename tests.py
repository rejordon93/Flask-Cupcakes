import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, Cupcake
from app import app


class CupcakeTestCase(unittest.TestCase):
    """Test case for Cupcake API"""

    def setUp(self):
        """Set up test case"""
        # Update the configuration of the Flask app
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_cupcakes.db"
        app.config["SQLALCHEMY_ECHO"] = False
        app.config["TESTING"] = True

        # Connect to the test database
        connect_db(app)

        # Create all tables
        db.create_all()

    def tearDown(self):
        """Tear down test case"""
        # Drop all tables
        db.drop_all()

    def test_create_cupcake(self):
        """Test creating a new cupcake"""
        # Create a new cupcake
        new_cupcake = {
            "flavor": "Test Flavor",
            "size": "Test Size",
            "rating": 5,
            "image": "test.jpg"
        }

        response = app.test_client().post("/cupcakes", json=new_cupcake)
        data = response.get_json()
        created_cupcake = data["cupcake"]

        # Check if the response status code is 201
        self.assertEqual(response.status_code, 201)
        # Check if the returned cupcake matches the input data
        self.assertEqual(created_cupcake["flavor"], new_cupcake["flavor"])
        self.assertEqual(created_cupcake["size"], new_cupcake["size"])
        self.assertEqual(created_cupcake["rating"], new_cupcake["rating"])
        self.assertEqual(created_cupcake["image"], new_cupcake["image"])

    def test_update_cupcake(self):
        """Test updating a cupcake with the PATCH route."""
        # Create a test cupcake
        cupcake = Cupcake(flavor="Test Flavor",
                          size="Test Size", rating=5, image="test.jpg")
        db.session.add(cupcake)
        db.session.commit()

        # Update the test cupcake with PATCH request
        updated_data = {
            "flavor": "Updated Flavor",
            "size": "Updated Size",
            "rating": 4,
            "image": "updated.jpg"
        }

        response = app.test_client().patch(
            f"/cupcakes/{cupcake.id}", json=updated_data)
        data = response.get_json()
        updated_cupcake = data["cupcake"]

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Check if the returned cupcake matches the updated data
        self.assertEqual(updated_cupcake["flavor"], updated_data["flavor"])
        self.assertEqual(updated_cupcake["size"], updated_data["size"])
        self.assertEqual(updated_cupcake["rating"], updated_data["rating"])
        self.assertEqual(updated_cupcake["image"], updated_data["image"])

    def test_update_cupcake_not_found(self):
        """Test updating a non-existent cupcake with the PATCH route."""
        # Update a non-existent cupcake with PATCH request
        updated_data = {
            "flavor": "Updated Flavor",
            "size": "Updated Size",
            "rating": 4,
            "image": "updated.jpg"
        }

        response = app.test_client().patch("/cupcakes/999", json=updated_data)
        data = response.get_json()

        # Check if the response status code is 404
        self.assertEqual(response)

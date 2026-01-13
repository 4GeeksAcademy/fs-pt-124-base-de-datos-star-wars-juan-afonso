from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import List

db = SQLAlchemy()

favorite_vehicles = db.Table( 
    "favorite_vehicles", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True), 
    db.Column("vehicle_id", db.Integer, db.ForeignKey("vehicles.id"), primary_key=True),
)

favorite_planets = db.Table( 
    "favorite_planets", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True), 
    db.Column("planet_id", db.Integer, db.ForeignKey("planets.id"), primary_key=True), 
)

favorite_droids = db.Table( 
    "favorite_droids", 
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True), 
    db.Column("droid_id", db.Integer, db.ForeignKey("droids.id"), primary_key=True), 
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    favorite_vehicles: Mapped[int] = mapped_column(nullable=False)
    favorite_planets: Mapped[int] = mapped_column(nullable=False)
    favorite_droids: Mapped[int] = mapped_column(nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicles: Mapped[List["Vehicles"]] = relationship()

    id: Mapped[int] = mapped_column(primary_key=True)
    planets: Mapped[List["Planets"]] = relationship()

    id: Mapped[int] = mapped_column(primary_key=True)
    droids: Mapped[List["Droids"]] = relationship()

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicles = db.relationship( 
        "Vehicles", 
        secondary=favorite_vehicles, 
        backref=db.backref("users_who_favorited", lazy="dynamic"), 
        lazy="dynamic" 
    )

    planets = db.relationship( 
        "Planets", 
        secondary=favorite_planets, 
        backref=db.backref("users_who_favorited", lazy="dynamic"), 
        lazy="dynamic" 
    )

    droids = db.relationship( 
        "Droids", 
        secondary=favorite_droids, 
        backref=db.backref("users_who_favorited", lazy="dynamic"), 
        lazy="dynamic" 
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Vehicles(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(unique=True, nullable=False)
    creator: Mapped[str] = mapped_column(unique=True, nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[List[User]] = relationship(secondary=favorite_vehicles)

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "creator": self.creator,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    population: Mapped[int] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "size": self.size,
            # do not serialize the password, its a security breach
        }
    
class Droids(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(unique=True, nullable=False)
    creator: Mapped[str] = mapped_column(unique=True, nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "creator": self.creator,
            # do not serialize the password, its a security breach
        }

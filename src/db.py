from typing import Dict, Tuple
from typing_extensions import Self
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


def create_db(uri: str) -> Tuple[Flask, SQLAlchemy]:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db = SQLAlchemy(app)
    return (app, db)


app, db = create_db("sqlite:///../data/sqlite.db")


class Posts(db.Model):
    __tablename__ = "posts"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer(), ForeignKey("users.id"))
    title = Column("title", String())
    body = Column("body", String())
    user = relationship("Users")

    def __init__(self, user_id: int, title: str, body: str) -> None:
        self.user_id = user_id
        self.title = title
        self.body = body

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "body": self.body,
        }

    @classmethod
    def from_json(cls, json: Dict) -> Self:
        return cls(json["userId"], json["title"], json["body"])


class Users(db.Model):
    __tablename__ = "users"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    name = Column("name", String())
    username = Column("username", String())
    email = Column("email", String())
    address = Column("address", ForeignKey("addresses.id"))
    phone = Column("phone", String())
    website = Column("website", String())
    company = Column("company", Integer(), ForeignKey("companies.id"))
    companies = relationship("Companies")
    addresses = relationship("Addresses")

    def __init__(
        self,
        id: int,
        name: str,
        username: str,
        email: str,
        address: int,
        phone: str,
        website: str,
        company: int,
    ) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.address = address
        self.phone = phone
        self.website = website
        self.company = company

    @classmethod
    def from_json(cls, json: Dict, address: int, company: int) -> Self:
        return cls(
            json["id"],
            json["name"],
            json["username"],
            json["email"],
            address,
            json["phone"],
            json["website"],
            company,
        )


class Companies(db.Model):
    __tablename__ = "companies"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    name = Column("name", String())
    catch_phrase = Column("catch_phrase", String())
    bs = Column("bs", String())

    def __init__(self, name: str, catch_phrase: str, bs: str) -> None:
        self.name = name
        self.catch_phrase = catch_phrase
        self.bs = bs

    @classmethod
    def from_json(cls, json: Dict) -> Self:
        return cls(json["name"], json["catchPhrase"], json["bs"])


class Addresses(db.Model):
    __tablename__ = "addresses"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    street = Column("street", String())
    suite = Column("suite", String())
    city = Column("city", String())
    zipcode = Column("zipcode", String())
    geo = Column("geo", Integer(), ForeignKey("coords.id"))
    rel = relationship("Coordinates")

    def __init__(
        self, street: str, suite: str, city: str, zipcode: str, geo: int
    ) -> None:
        self.street = street
        self.suite = suite
        self.city = city
        self.zipcode = zipcode
        self.geo = geo

    @classmethod
    def from_json(cls, json: Dict, geo: int) -> Self:
        return cls(
            json["street"], json["suite"], json["city"], json["zipcode"], geo
        )


class Coordinates(db.Model):
    __tablename__ = "coords"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    lat = Column("lat", Float())
    lon = Column("lon", Float())

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    @classmethod
    def from_json(cls, json: Dict) -> Self:
        return cls(json["lat"], json["lng"])

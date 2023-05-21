from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))



class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    references = db.Column(db.String(200), nullable=True)
    contact_number = db.Column(db.String(20), nullable=False)
    gcse_passes = db.Column(db.Integer, nullable=False)
    education_level = db.Column(db.Integer, nullable=False)
    past_experience = db.Column(db.String(500), nullable=True)

    candidate = db.relationship('Candidate', backref=db.backref('cv', lazy=True, uselist=False))
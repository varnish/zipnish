from . import db

class Spans(db.Model):
    __tablename__ = 'zipkin_spans'

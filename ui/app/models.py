from . import db

class Spans(db.Model):
    __tablename__ = 'zipkin_spans'
    span_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer)
    trace_id = db.Column(db.Integer)
    span_name = db.Column(db.String(255))
    debug = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    created_ts = db.Column(db.Integer)

class Annotations(db.Model):
    __tablename__ = 'zipkin_annotations'

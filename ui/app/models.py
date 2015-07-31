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

    def __repr__(self):
        return '<Span %r>' % self.span_name

class Annotations(db.Model):
    __tablename__ = 'zipkin_annotations'
    span_id = db.Column(db.Integer)
    trace_id = db.Column(db.Integer)
    span_name = db.Column(db.String(255))
    service_name = db.Column(db.String(255))
    value = db.Column(db.Text)
    ipv4 = db.Column(db.Integer)
    port = db.Column(db.Integer)
    a_timestamp = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    def __repr__(self):
        return '<Annotation %r - %r>' % (self.span_name, self.service_name)

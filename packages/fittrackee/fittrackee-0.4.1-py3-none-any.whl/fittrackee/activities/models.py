import datetime
import os
from uuid import uuid4

from fittrackee import db
from sqlalchemy.dialects import postgresql
from sqlalchemy.event import listens_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.session import object_session
from sqlalchemy.types import JSON, Enum

from .utils_files import get_absolute_file_path
from .utils_format import convert_in_duration, convert_value_to_integer
from .utils_id import encode_uuid

record_types = [
    'AS',  # 'Best Average Speed'
    'FD',  # 'Farthest Distance'
    'LD',  # 'Longest Duration'
    'MS',  # 'Max speed'
]


def update_records(user_id, sport_id, connection, session):
    record_table = Record.__table__
    new_records = Activity.get_user_activity_records(user_id, sport_id)
    for record_type, record_data in new_records.items():
        if record_data['record_value']:
            record = Record.query.filter_by(
                user_id=user_id, sport_id=sport_id, record_type=record_type
            ).first()
            if record:
                value = convert_value_to_integer(
                    record_type, record_data['record_value']
                )
                connection.execute(
                    record_table.update()
                    .where(record_table.c.id == record.id)
                    .values(
                        value=value,
                        activity_id=record_data['activity'].id,
                        activity_uuid=record_data['activity'].uuid,
                        activity_date=record_data['activity'].activity_date,
                    )
                )
            else:
                new_record = Record(
                    activity=record_data['activity'], record_type=record_type
                )
                new_record.value = record_data['record_value']
                session.add(new_record)
        else:
            connection.execute(
                record_table.delete()
                .where(record_table.c.user_id == user_id)
                .where(record_table.c.sport_id == sport_id)
                .where(record_table.c.record_type == record_type)
            )


class Sport(db.Model):
    __tablename__ = "sports"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(50), unique=True, nullable=False)
    img = db.Column(db.String(255), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    activities = db.relationship(
        'Activity', lazy=True, backref=db.backref('sports', lazy='joined')
    )
    records = db.relationship(
        'Record', lazy=True, backref=db.backref('sports', lazy='joined')
    )

    def __repr__(self):
        return f'<Sport {self.label!r}>'

    def __init__(self, label):
        self.label = label

    def serialize(self, is_admin=False):
        serialized_sport = {
            'id': self.id,
            'label': self.label,
            'img': self.img,
            'is_active': self.is_active,
        }
        if is_admin:
            serialized_sport['has_activities'] = len(self.activities) > 0
        return serialized_sport


class Activity(db.Model):
    __tablename__ = "activities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(
        postgresql.UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport_id = db.Column(
        db.Integer, db.ForeignKey('sports.id'), nullable=False
    )
    title = db.Column(db.String(255), nullable=True)
    gpx = db.Column(db.String(255), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modification_date = db.Column(
        db.DateTime, onupdate=datetime.datetime.utcnow
    )
    activity_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Interval, nullable=False)
    pauses = db.Column(db.Interval, nullable=True)
    moving = db.Column(db.Interval, nullable=True)
    distance = db.Column(db.Numeric(6, 3), nullable=True)  # kilometers
    min_alt = db.Column(db.Numeric(6, 2), nullable=True)  # meters
    max_alt = db.Column(db.Numeric(6, 2), nullable=True)  # meters
    descent = db.Column(db.Numeric(7, 2), nullable=True)  # meters
    ascent = db.Column(db.Numeric(7, 2), nullable=True)  # meters
    max_speed = db.Column(db.Numeric(6, 2), nullable=True)  # km/h
    ave_speed = db.Column(db.Numeric(6, 2), nullable=True)  # km/h
    bounds = db.Column(postgresql.ARRAY(db.Float), nullable=True)
    map = db.Column(db.String(255), nullable=True)
    map_id = db.Column(db.String(50), nullable=True)
    weather_start = db.Column(JSON, nullable=True)
    weather_end = db.Column(JSON, nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    segments = db.relationship(
        'ActivitySegment',
        lazy=True,
        cascade='all, delete',
        backref=db.backref('activities', lazy='joined', single_parent=True),
    )
    records = db.relationship(
        'Record',
        lazy=True,
        cascade='all, delete',
        backref=db.backref('activities', lazy='joined', single_parent=True),
    )

    def __str__(self):
        return f'<Activity \'{self.sports.label}\' - {self.activity_date}>'

    def __init__(self, user_id, sport_id, activity_date, distance, duration):
        self.user_id = user_id
        self.sport_id = sport_id
        self.activity_date = activity_date
        self.distance = distance
        self.duration = duration

    @property
    def short_id(self):
        return encode_uuid(self.uuid)

    def serialize(self, params=None):
        date_from = params.get('from') if params else None
        date_to = params.get('to') if params else None
        distance_from = params.get('distance_from') if params else None
        distance_to = params.get('distance_to') if params else None
        duration_from = params.get('duration_from') if params else None
        duration_to = params.get('duration_to') if params else None
        ave_speed_from = params.get('ave_speed_from') if params else None
        ave_speed_to = params.get('ave_speed_to') if params else None
        max_speed_from = params.get('max_speed_from') if params else None
        max_speed_to = params.get('max_speed_to') if params else None
        sport_id = params.get('sport_id') if params else None
        previous_activity = (
            Activity.query.filter(
                Activity.id != self.id,
                Activity.user_id == self.user_id,
                Activity.sport_id == sport_id if sport_id else True,
                Activity.activity_date <= self.activity_date,
                Activity.activity_date
                >= datetime.datetime.strptime(date_from, '%Y-%m-%d')
                if date_from
                else True,
                Activity.activity_date
                <= datetime.datetime.strptime(date_to, '%Y-%m-%d')
                if date_to
                else True,
                Activity.distance >= int(distance_from)
                if distance_from
                else True,
                Activity.distance <= int(distance_to) if distance_to else True,
                Activity.duration >= convert_in_duration(duration_from)
                if duration_from
                else True,
                Activity.duration <= convert_in_duration(duration_to)
                if duration_to
                else True,
                Activity.ave_speed >= float(ave_speed_from)
                if ave_speed_from
                else True,
                Activity.ave_speed <= float(ave_speed_to)
                if ave_speed_to
                else True,
                Activity.max_speed >= float(max_speed_from)
                if max_speed_from
                else True,
                Activity.max_speed <= float(max_speed_to)
                if max_speed_to
                else True,
            )
            .order_by(Activity.activity_date.desc())
            .first()
        )
        next_activity = (
            Activity.query.filter(
                Activity.id != self.id,
                Activity.user_id == self.user_id,
                Activity.sport_id == sport_id if sport_id else True,
                Activity.activity_date >= self.activity_date,
                Activity.activity_date
                >= datetime.datetime.strptime(date_from, '%Y-%m-%d')
                if date_from
                else True,
                Activity.activity_date
                <= datetime.datetime.strptime(date_to, '%Y-%m-%d')
                if date_to
                else True,
                Activity.distance >= int(distance_from)
                if distance_from
                else True,
                Activity.distance <= int(distance_to) if distance_to else True,
                Activity.duration >= convert_in_duration(duration_from)
                if duration_from
                else True,
                Activity.duration <= convert_in_duration(duration_to)
                if duration_to
                else True,
                Activity.ave_speed >= float(ave_speed_from)
                if ave_speed_from
                else True,
                Activity.ave_speed <= float(ave_speed_to)
                if ave_speed_to
                else True,
            )
            .order_by(Activity.activity_date.asc())
            .first()
        )
        return {
            "id": self.short_id,  # WARNING: client use uuid as id
            "user": self.user.username,
            "sport_id": self.sport_id,
            "title": self.title,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
            "activity_date": self.activity_date,
            "duration": str(self.duration) if self.duration else None,
            "pauses": str(self.pauses) if self.pauses else None,
            "moving": str(self.moving) if self.moving else None,
            "distance": float(self.distance) if self.distance else None,
            "min_alt": float(self.min_alt) if self.min_alt else None,
            "max_alt": float(self.max_alt) if self.max_alt else None,
            "descent": float(self.descent) if self.descent else None,
            "ascent": float(self.ascent) if self.ascent else None,
            "max_speed": float(self.max_speed) if self.max_speed else None,
            "ave_speed": float(self.ave_speed) if self.ave_speed else None,
            "with_gpx": self.gpx is not None,
            "bounds": [float(bound) for bound in self.bounds]
            if self.bounds
            else [],  # noqa
            "previous_activity": previous_activity.short_id
            if previous_activity
            else None,  # noqa
            "next_activity": next_activity.short_id if next_activity else None,
            "segments": [segment.serialize() for segment in self.segments],
            "records": [record.serialize() for record in self.records],
            "map": self.map_id if self.map else None,
            "weather_start": self.weather_start,
            "weather_end": self.weather_end,
            "notes": self.notes,
        }

    @classmethod
    def get_user_activity_records(cls, user_id, sport_id, as_integer=False):
        record_types_columns = {
            'AS': 'ave_speed',  # 'Average speed'
            'FD': 'distance',  # 'Farthest Distance'
            'LD': 'moving',  # 'Longest Duration'
            'MS': 'max_speed',  # 'Max speed'
        }
        records = {}
        for record_type, column in record_types_columns.items():
            column_sorted = getattr(getattr(Activity, column), 'desc')()
            record_activity = (
                Activity.query.filter_by(user_id=user_id, sport_id=sport_id)
                .order_by(column_sorted, Activity.activity_date)
                .first()
            )
            records[record_type] = dict(
                record_value=(
                    getattr(record_activity, column)
                    if record_activity
                    else None
                ),
                activity=record_activity,
            )
        return records


@listens_for(Activity, 'after_insert')
def on_activity_insert(mapper, connection, activity):
    @listens_for(db.Session, 'after_flush', once=True)
    def receive_after_flush(session, context):
        update_records(
            activity.user_id, activity.sport_id, connection, session
        )  # noqa


@listens_for(Activity, 'after_update')
def on_activity_update(mapper, connection, activity):
    if object_session(activity).is_modified(
        activity, include_collections=True
    ):  # noqa

        @listens_for(db.Session, 'after_flush', once=True)
        def receive_after_flush(session, context):
            sports_list = [activity.sport_id]
            records = Record.query.filter_by(activity_id=activity.id).all()
            for rec in records:
                if rec.sport_id not in sports_list:
                    sports_list.append(rec.sport_id)
            for sport_id in sports_list:
                update_records(activity.user_id, sport_id, connection, session)


@listens_for(Activity, 'after_delete')
def on_activity_delete(mapper, connection, old_record):
    @listens_for(db.Session, 'after_flush', once=True)
    def receive_after_flush(session, context):
        if old_record.map:
            os.remove(get_absolute_file_path(old_record.map))
        if old_record.gpx:
            os.remove(get_absolute_file_path(old_record.gpx))


class ActivitySegment(db.Model):
    __tablename__ = "activity_segments"
    activity_id = db.Column(
        db.Integer, db.ForeignKey('activities.id'), primary_key=True
    )
    activity_uuid = db.Column(postgresql.UUID(as_uuid=True), nullable=False)
    segment_id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Interval, nullable=False)
    pauses = db.Column(db.Interval, nullable=True)
    moving = db.Column(db.Interval, nullable=True)
    distance = db.Column(db.Numeric(6, 3), nullable=True)  # kilometers
    min_alt = db.Column(db.Numeric(6, 2), nullable=True)  # meters
    max_alt = db.Column(db.Numeric(6, 2), nullable=True)  # meters
    descent = db.Column(db.Numeric(7, 2), nullable=True)  # meters
    ascent = db.Column(db.Numeric(7, 2), nullable=True)  # meters
    max_speed = db.Column(db.Numeric(6, 2), nullable=True)  # km/h
    ave_speed = db.Column(db.Numeric(6, 2), nullable=True)  # km/h

    def __str__(self):
        return (
            f'<Segment \'{self.segment_id}\' '
            f'for activity \'{encode_uuid(self.activity_uuid)}\'>'
        )

    def __init__(self, segment_id, activity_id, activity_uuid):
        self.segment_id = segment_id
        self.activity_id = activity_id
        self.activity_uuid = activity_uuid

    def serialize(self):
        return {
            "activity_id": encode_uuid(self.activity_uuid),
            "segment_id": self.segment_id,
            "duration": str(self.duration) if self.duration else None,
            "pauses": str(self.pauses) if self.pauses else None,
            "moving": str(self.moving) if self.moving else None,
            "distance": float(self.distance) if self.distance else None,
            "min_alt": float(self.min_alt) if self.min_alt else None,
            "max_alt": float(self.max_alt) if self.max_alt else None,
            "descent": float(self.descent) if self.descent else None,
            "ascent": float(self.ascent) if self.ascent else None,
            "max_speed": float(self.max_speed) if self.max_speed else None,
            "ave_speed": float(self.ave_speed) if self.ave_speed else None,
        }


class Record(db.Model):
    __tablename__ = "records"
    __table_args__ = (
        db.UniqueConstraint(
            'user_id', 'sport_id', 'record_type', name='user_sports_records'
        ),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sport_id = db.Column(
        db.Integer, db.ForeignKey('sports.id'), nullable=False
    )
    activity_id = db.Column(
        db.Integer, db.ForeignKey('activities.id'), nullable=False
    )
    activity_uuid = db.Column(postgresql.UUID(as_uuid=True), nullable=False)
    record_type = db.Column(Enum(*record_types, name="record_types"))
    activity_date = db.Column(db.DateTime, nullable=False)
    _value = db.Column("value", db.Integer, nullable=True)

    def __str__(self):
        return (
            f'<Record {self.sports.label} - '
            f'{self.record_type} - '
            f"{self.activity_date.strftime('%Y-%m-%d')}>"
        )

    def __init__(self, activity, record_type):
        self.user_id = activity.user_id
        self.sport_id = activity.sport_id
        self.activity_id = activity.id
        self.activity_uuid = activity.uuid
        self.record_type = record_type
        self.activity_date = activity.activity_date

    @hybrid_property
    def value(self):
        if self._value is None:
            return None
        if self.record_type == 'LD':
            return datetime.timedelta(seconds=self._value)
        elif self.record_type in ['AS', 'MS']:
            return float(self._value / 100)
        else:  # 'FD'
            return float(self._value / 1000)

    @value.setter
    def value(self, val):
        self._value = convert_value_to_integer(self.record_type, val)

    def serialize(self):
        if self.value is None:
            value = None
        elif self.record_type in ['AS', 'FD', 'MS']:
            value = float(self.value)
        else:  # 'LD'
            value = str(self.value)

        return {
            "id": self.id,
            "user": self.user.username,
            "sport_id": self.sport_id,
            "activity_id": encode_uuid(self.activity_uuid),
            "record_type": self.record_type,
            "activity_date": self.activity_date,
            "value": value,
        }


@listens_for(Record, 'after_delete')
def on_record_delete(mapper, connection, old_record):
    @listens_for(db.Session, 'after_flush', once=True)
    def receive_after_flush(session, context):
        activity = old_record.activities
        new_records = Activity.get_user_activity_records(
            activity.user_id, activity.sport_id
        )
        for record_type, record_data in new_records.items():
            if (
                record_data['record_value']
                and record_type == old_record.record_type
            ):
                new_record = Record(
                    activity=record_data['activity'], record_type=record_type
                )
                new_record.value = record_data['record_value']
                session.add(new_record)

from app.extensions import db
from app.domain.value_objects import ArtistType, MusicGenre, Name, Text100
from app.models.music_event import event_artist
from sqlalchemy.ext.hybrid import hybrid_property


class Artist(db.Model):
    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, primary_key=True)
    _first_name = db.Column("first_name", db.String(30), nullable=False)
    _second_name = db.Column("second_name", db.String(30), nullable=False)
    _artist_type = db.Column("artist_type", db.String(80), nullable=False)
    _music_genre = db.Column("music_genre", db.String(80), nullable=False)
    _bio = db.Column("bio", db.String(100))

    events = db.relationship("MusicEvent", secondary=event_artist, back_populates="artists")

    @hybrid_property
    def first_name(self) -> Name:
        return Name(self._first_name)

    @first_name.expression
    def first_name(cls):
        return cls._first_name

    @first_name.setter
    def first_name(self, value: Name) -> None:
        if not isinstance(value, Name):
            raise TypeError("first_name must be a Name value object")
        self._first_name = value.value

    @hybrid_property
    def second_name(self) -> Name:
        return Name(self._second_name)

    @second_name.expression
    def second_name(cls):
        return cls._second_name

    @second_name.setter
    def second_name(self, value: Name) -> None:
        if not isinstance(value, Name):
            raise TypeError("second_name must be a Name value object")
        self._second_name = value.value

    @hybrid_property
    def artist_type(self) -> ArtistType:
        return ArtistType(self._artist_type)

    @artist_type.expression
    def artist_type(cls):
        return cls._artist_type

    @artist_type.setter
    def artist_type(self, value: ArtistType) -> None:
        if not isinstance(value, ArtistType):
            raise TypeError("artist_type must be an ArtistType value object")
        self._artist_type = value.value

    @hybrid_property
    def music_genre(self) -> MusicGenre:
        return MusicGenre(self._music_genre)

    @music_genre.expression
    def music_genre(cls):
        return cls._music_genre

    @music_genre.setter
    def music_genre(self, value: MusicGenre) -> None:
        if not isinstance(value, MusicGenre):
            raise TypeError("music_genre must be a MusicGenre value object")
        self._music_genre = value.value

    @hybrid_property
    def bio(self) -> Text100:
        return Text100(self._bio or "")

    @bio.expression
    def bio(cls):
        return cls._bio

    @bio.setter
    def bio(self, value: Text100) -> None:
        if not isinstance(value, Text100):
            raise TypeError("bio must be a Text100 value object")
        self._bio = value.value

    def updateProfile(self, first_name: Name, second_name: Name, bio: Text100) -> bool:
        self.first_name = first_name
        self.second_name = second_name
        self.bio = bio
        db.session.commit()
        return True

    def viewEvents(self) -> list:
        return [event.event_id for event in self.events]

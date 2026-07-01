from app.domain.value_objects import ArtistType, MusicGenre, Name, Text100
from app.extensions import db
from app.models.music_event import event_artist


class Artist(db.Model):
    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, primary_key=True)
    _first_name = db.Column("first_name", db.String(30), nullable=False)
    _second_name = db.Column("second_name", db.String(30), nullable=False)
    _artist_type = db.Column("artist_type", db.String(80), nullable=False)
    _music_genre = db.Column("music_genre", db.String(80), nullable=False)
    _bio = db.Column("bio", db.String(100))

    events = db.relationship("MusicEvent", secondary=event_artist, back_populates="artists")

    @property
    def first_name(self) -> Name:
        return Name(self._first_name)

    @first_name.setter
    def first_name(self, value: Name | str) -> None:
        first_name = value if isinstance(value, Name) else Name(value)
        self._first_name = first_name.value

    @property
    def second_name(self) -> Name:
        return Name(self._second_name)

    @second_name.setter
    def second_name(self, value: Name | str) -> None:
        second_name = value if isinstance(value, Name) else Name(value)
        self._second_name = second_name.value

    @property
    def artist_type(self) -> ArtistType:
        return ArtistType(self._artist_type)

    @artist_type.setter
    def artist_type(self, value: ArtistType | str) -> None:
        artist_type = value if isinstance(value, ArtistType) else ArtistType(value)
        self._artist_type = artist_type.value

    @property
    def music_genre(self) -> MusicGenre:
        return MusicGenre(self._music_genre)

    @music_genre.setter
    def music_genre(self, value: MusicGenre | str) -> None:
        music_genre = value if isinstance(value, MusicGenre) else MusicGenre(value)
        self._music_genre = music_genre.value

    @property
    def bio(self) -> Text100:
        return Text100(self._bio or "")

    @bio.setter
    def bio(self, value: Text100 | str) -> None:
        bio = value if isinstance(value, Text100) else Text100(value)
        self._bio = bio.value

    def updateProfile(self, first_name: Name | str, second_name: Name | str, bio: Text100 | str) -> bool:
        return

    def viewEvents(self) -> list[int]:
        return

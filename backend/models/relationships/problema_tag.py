from sqlalchemy import Column, Integer, Table, ForeignKey
from database import Base


problema_tag_relationship = Table(
    'problema_tag',
    Base.metadata,
    Column(
        'problema_id',
        Integer,
        ForeignKey('problemas.id')),

    Column(
        'tag_id',
        Integer,
        ForeignKey('tags.id'))
)

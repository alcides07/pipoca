from sqlalchemy import Column, Integer, Table, ForeignKey
from database import Base


problema_tag_relationship = Table(
    'problema_tag',
    Base.metadata,
    Column(
        'problema_id',
        Integer,
        ForeignKey(
            'problemas.id',
            name="problema_tag_problema_id_fkey"
        )
    ),

    Column(
        'tag_id',
        Integer,
        ForeignKey(
            'tags.id',
            name="problema_tag_tag_id_fkey"
        )
    )
)

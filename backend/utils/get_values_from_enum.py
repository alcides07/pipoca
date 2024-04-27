def get_values_from_enum(enum):
    values = ', '.join(
        [value.value for value in enum]
    )

    return values

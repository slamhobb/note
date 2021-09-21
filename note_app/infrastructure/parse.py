def get_bool(key: str) -> bool:
    return {'True': True, 'False': False}.get(key, False)

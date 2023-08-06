def default_flow() -> dict:
    """Create a empty flow to be used for defaults

    Returns:
        dict: Empty Flow Dictionary
    """
    return {
        "offset": {
            "x": 0,
            "y": 0,
        },
        "scale": 1,
        "nodes": {},
        "links": {},
        "selected": {},
        "hovered": {},
        "editing": None,
    }
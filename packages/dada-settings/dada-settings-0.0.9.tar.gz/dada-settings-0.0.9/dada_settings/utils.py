from typing import NewType, List, Dict, Any


FieldsList = NewType("FieldsList", List[Dict[str, Any]])


def join_fields(prefix: str, fields: FieldsList, props: Dict[str, Any]) -> FieldsList:
    """
    Join and prefix a list of fields with default properties
    :param prefix: The prefix to prepend to the keys of the fields
    :param fields: A dictionary of key/value fields
    :param props: A dictionary of props to join by default
    :return dict
    """
    out_fields = []
    for f in fields:
        combined = dict(list(f.items()) + list(props.items()))
        name = combined.get("name")
        if not name:
            raise ValueError(
                f"Could not construct {prefix} field because it was missing a name: {combined}"
            )

        # prefix the name
        combined["name"] = f"{prefix}_{name}"
        out_fields.append(combined)

    return out_fields

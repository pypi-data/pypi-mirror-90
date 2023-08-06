from enum import EnumMeta

try:
    import enums
except ImportError:
    print("Couldn't find your enums file")


def validate(schema) -> (bool, str):
    for field in schema.Config.fields:
        for enum_name in dir(enums):
            enum = getattr(enums, enum_name)
            try:
                if enum is not None and issubclass(type(enum), EnumMeta):
                    if str(field).capitalize() == enum_name:
                        value = getattr(schema, field)
                        values = [v.value for v in enum]
                        if value in values:
                            return True, ""
                        else:
                            return False, f"'{value}' not in accepted values: {values}"
            except TypeError:
                print("Not an enum")

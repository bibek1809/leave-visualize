import json

class ObjectMapper:
    def map_to(self, json_data, cls):
        if isinstance(json_data, list):
            return [cls(**item) for item in json_data]
        return cls(**json_data)

    def to_json(self, cls):
        # Ensure cls is an instance with a to_dict method or similar
        if hasattr(cls, 'to_dict'):
            return json.dumps(cls.to_dict())
        raise ValueError("The provided class does not have a 'to_dict' method")


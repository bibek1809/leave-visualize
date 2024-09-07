import json
class ObjectMapper:

    def map_to(self, json_data, cls):
        return cls(**json_data)

    def to_json(self, cls):
        return json(cls)

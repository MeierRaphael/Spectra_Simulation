import json
import matlab

class MatlabDoubleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, matlab.double):
            if obj.size == (1, 1):
                return obj[0][0]
            return list(obj)
        return json.JSONEncoder.default(self, obj)
"""
@file
@brief Helpers about :epkg:`json`.
"""
import pprint
import numpy
import ujson


class JsonError(ValueError):
    """
    Raised when serialization to json does not work.
    """

    def __init__(self, obj, data=None):

        msg = pprint.pformat(obj)
        if len(msg) > 2000:
            msg = msg[:2000] + "\n..."
        msg2 = pprint.pformat(data)
        if len(msg2) > 2000:
            msg2 = msg2[:2000] + "\n..."
        ValueError.__init__(
            self, "Unable to serialize object of type '{}' into json.\n{}\n----\n{}".format(
                type(obj), msg, msg2))


def json_dumps(obj):
    """
    Dumps an object into :epkg:`json`.

    @param      X       object
    @return             json
    """
    def _modify(o):
        return dict(shape=o.shape, dtype=str(o.dtype),
                    data=o.tolist(), ___=1)

    if isinstance(obj, numpy.ndarray):
        obj = _modify(obj)
    elif isinstance(obj, dict):
        obj = {k: (_modify(v) if isinstance(v, numpy.ndarray) else v)
               for k, v in obj.items()}
    try:
        return ujson.dumps(obj, reject_bytes=False)
    except UnicodeDecodeError:
        raise JsonError(obj)


def json_loads(jsdata):
    """
    Loads an object from :epkg:`json`.

    @param      jsdata      json
    @return                 object
    """
    obj = ujson.loads(jsdata)
    if isinstance(obj, dict):
        if '___' in obj:
            # numpy array
            shape = obj['shape']
            obj = numpy.array(obj['data'], dtype=obj['dtype'])
            obj = obj.reshape(tuple(shape))
        else:
            up = {}
            for k, v in obj.items():
                if isinstance(v, dict) and '___' in v:
                    shape = v['shape']
                    v = numpy.array(v['data'], dtype=v['dtype'])
                    v = v.reshape(tuple(shape))
                    up[k] = v
            obj.update(up)
    return obj

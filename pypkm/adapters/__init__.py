# coding=utf-8

"""General Purpose Adapters"""

class DateAdapter(Adapter):
    def _encode(self, obj, ctx):
        """Converts a 3-item tuple into date byte data."""

        # we need a throwaway class because dates are substructed so
        # they require _encode to return an object with all the proper
        # attributes set
        class _Obj(object):
            pass
        
        _obj = _Obj()
        _obj.year = obj[0]
        if obj[0] > 2000:
            _obj.year -= 2000
        _obj.month = obj[1]
        _obj.day = obj[2]

        return _obj
    
    def _decode(self, obj, ctx):
        """Converts date byte data into a 3-item tuple."""

        return (obj.year + 2000, obj.month, obj.day)
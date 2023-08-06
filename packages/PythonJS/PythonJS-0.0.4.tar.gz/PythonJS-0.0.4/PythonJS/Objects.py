
class Object:
    def __init__(self, obj=None):
        if not obj:
            return
        else:
            attrs = obj.attributes()
            for attr in attrs:
                setattr(self, attr, obj.get_value(attr))
        return

    def attributes(self):
        attrs = self.__dir__()
        userattrs = []
        for attr in attrs:
            if "__" not in attr:
                userattrs.append(attr)
        return userattrs

    def values(self):
        attrs = self.attributes()
        values = []
        for attr in attrs:
            values.append(self.get_value(attr))
        return values

    def set_attribute(self, attr, value):
        setattr(self, attr, value)
        return self

    def get_value(self, attr):
        getattr(self, attr)
        return self

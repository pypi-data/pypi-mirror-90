class Object:
    def __init__(self, obj=None, name=None):
        self.__methods = []  # 'attributes', 'values', 'set_attribute', 'get_value'
        self.__class_attrs = []
        self.__setup_object()
        self.__name = name if name else id(self)
        if not obj:
            return
        else:
            attrs = obj.attributes()
            for attr in attrs:
                setattr(self, attr, obj.get_value(attr))
        return

    def __setup_object(self):
        attrs = self.__dir__()
        method_type = type(self.get_value('attributes'))
        for attr in attrs:
            if "__" not in attr:
                attr_type = type(self.get_value(attr))
                if attr_type == method_type:
                    self.__methods.append(attr)
                else:
                    self.__class_attrs.append(attr)

    def attributes(self):
        attrs = self.__dir__()
        user_attrs = []
        for attr in attrs:
            if "__" not in attr and attr not in self.__methods and attr not in self.__class_attrs:
                user_attrs.append(attr)
        return user_attrs

    def values(self):
        attrs = self.attributes()
        values = []
        for attr in attrs:
            values.append(self.get_value(attr))
        return values

    def set_attribute(self, attr, value):
        return self.__setattr__(attr, value)

    def get_value(self, attr):
        return self.__getattribute__(attr)

    def __getitem__(self, attr):
        return self.get_value(attr)

    def __console_output(self):
        attrs = self.attributes()
        object_output = ""
        for attr in attrs:
            object_output += "\n\t" + attr + ": " + str(self.get_value(attr))

        display_output = "{ObjName}<Object>: {openBracket} \n {ObjOut} \n {closedBracket}".format(ObjName=self.__name,
                                                                                                  openBracket="{",
                                                                                                  ObjOut=object_output,
                                                                                                  closedBracket="}")

        return display_output

    def __str__(self):
        return self.__console_output()

    def __repr__(self):
        return self.__console_output()

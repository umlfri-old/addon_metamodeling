class ValueValidator():

    @staticmethod
    def validate(value, element):
        if value.startswith('#self.'):
            for d in eval(element.values['attributes']):
                if value[6:] == d['attName'].replace(' ',''):
                    return True
            return False
        return True
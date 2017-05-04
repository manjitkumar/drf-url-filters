
def csv_validator(validator, invalid_msg, msg=None):
    '''
    Checks if each item in list of items matches voluptuous validator
    '''
    def fn(value):
        try:
            value = strip_list(validator(), value)
            return value
        except ValueError:
            raise Invalid('<{0}> '.format(value) + invalid_msg.format(value))

return fn
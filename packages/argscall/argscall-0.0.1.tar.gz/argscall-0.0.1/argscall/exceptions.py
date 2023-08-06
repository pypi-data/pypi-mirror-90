class MissingArgument(Exception):
    def __init__(self, argument_name, message="Missing required argument"):
        self.argument_name = argument_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.argument_name}"


class TooManyArgument(Exception):
    def __init__(self, argument_value, message="Got more arguments than expected"):
        self.argument_value = argument_value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} (value: '{self.argument_value}')"


class UnsupportedKeyArgument(Exception):
    def __init__(self, argument_name, message="Unsupported keyword argument"):
        self.argument_name = argument_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.argument_name}"

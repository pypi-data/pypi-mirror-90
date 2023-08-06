class BoardConfiguration:
    """
    Define a fine-grained configuration for your board
    """
    def __init__(self, model_pattern, label=None, **kwargs):
        self.model_pattern = model_pattern
        self.label = label
        self.cli_params = kwargs

    def __str__(self):
        """
        Return a readable representation of the board configuration
        """
        if self.label:
            return self.label
        params_string = ','.join(['%s=%s' % (k, str(v)) for k, v in self.cli_params.items()])
        return '%s {%s}' % (self.model_pattern, params_string)
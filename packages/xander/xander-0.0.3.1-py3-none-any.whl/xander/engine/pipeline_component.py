class Component:

    def __init__(self, function, params, storage_manager, logger, outputs,
                 undefined_output_number=False, destination_path=None):

        self.function = function
        self.params = params
        self.storage_manager = storage_manager
        self.logger = logger
        self.output_names = outputs
        self.undefined_output_number = undefined_output_number
        self.destination_path = destination_path

    def run(self):
        params_list = []

        for type, params in self.params:
            if type == 'file':
                params_list.append(self.storage_manager.get_file(filename=params))
            else:
                params_list.append(params)

        # Run the component function
        outputs = self.function(*params_list)

        return outputs

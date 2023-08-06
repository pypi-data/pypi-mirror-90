from datetime import datetime
import os
import uuid
import pandas as pd

from xander.engine.pipeline_component import Component


def define_output_names(outputs, output_names, pipeline_slug):
    names = output_names
    new_outputs = []

    if isinstance(outputs, list) and len(outputs) >= len(output_names):

        for i, output in enumerate(outputs):
            if i >= len(output_names):
                if isinstance(output, tuple) and isinstance(output[0], str) and isinstance(output[1], pd.DataFrame):
                    names.append(output[0])
                else:
                    names.append(os.path.join(pipeline_slug, pipeline_slug + datetime.now().strftime("%Y%m%d_%H%M%S")))
            new_outputs.append(output[1])

    elif isinstance(outputs, tuple) and len(outputs) == 2 and isinstance(outputs[0], str):
        names = [outputs[0]]
        new_outputs.append(outputs[1])

    else:
        raise Exception

    return new_outputs, names

class Pipeline:

    def __init__(self, name, logger, storage_manager):
        # Unique identifier of the pipeline.
        self.pipeline_id = uuid.uuid4().hex

        # Name of the pipeline provided by the user.
        self.pipeline_name = name

        # Slug of the pipeline to better represent it in the system.
        self.pipeline_slug = '_'.join(self.pipeline_name.split(' ')).lower()

        # List of methods to be applied in the pipeline. If the pipeline performs correctly they are saved and reloaded
        # on cold start.
        self.components = []

        # Logger manager, it can be None
        self.logger = logger

        # Storge manager
        self.storage_manager = storage_manager

    def run(self):
        """
        Run the pipeline using all specified methods.

        :return: True if the execution has terminated successfully, otherwise False.
        """

        for i, component in enumerate(self.components):
            self.logger.info("{}: component {}/{}".format(self.pipeline_slug, i + 1, len(self.components)))
            outputs = component.run()

            outputs, output_names = define_output_names(outputs, component.output_names, self.pipeline_slug)

            self.storage_manager.export(outputs=outputs, output_names=output_names)

        return True

    def add_component(self, function, params, outputs=None):
        component = Component(function=function, params=params, storage_manager=self.storage_manager,
                              logger=self.logger, outputs=outputs if outputs else [])

        self.components.append(component)

        self.logger.info('Pipeline {} -> new component added.'.format(self.pipeline_slug))

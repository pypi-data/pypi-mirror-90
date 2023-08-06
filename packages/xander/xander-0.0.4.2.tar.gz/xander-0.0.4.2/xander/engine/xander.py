import json

from xander.engine.client import XanderClient
from xander.engine.pipeline import Pipeline
from xander.engine.storage_manager import StorageManager
from xander.utils.logger import Logger


class XanderEngine:
    """
    The core of ML OPS tool.
    It is the object to be initialized by the user.
    """

    def __init__(self, local_source, local_destination, api_auth_file='zoe_sapphire.json'):
        """
        Class constructor.

        :param local_source: source folder in the local device
        :param local_destination: destination folder in the local device
        :param api_auth_file: authentication file to connect to cloud server
        """

        # Initialize the log manager
        self.logger = Logger()
        self.client = None

        self.logger.success('Zoe ML Engine is ready.')

        # Try to find the api auth file, otherwise run the Engine in local mode
        try:
            api_auth_file = json.load(open(api_auth_file, 'r'))
            self.client = XanderClient(api=api_auth_file, logger=self.logger)

            self.logger.info('Cloud mode is active.')
        except:
            self.logger.info('Local mode is active, API auth file not found!')

        # Initialize the storage manager
        self.storage_manager = StorageManager(local_source=local_source, local_destination=local_destination,
                                              logger=self.logger)

        # Initialize the pipelines list
        self.pipelines = []

    def run(self):
        """
        Run the engine. All pipelines are executed with their components.

        @return: None
        """

        self.logger.success("Terna ML Engine is running.")

        for i, pipeline in enumerate(self.pipelines):
            self.logger.info("({}/{}) Running '{}'".format(i + 1, len(self.pipelines), pipeline.pipeline_slug))
            pipeline.run()
            self.logger.info("Completed '{}'.".format(pipeline.pipeline_slug))

        self.logger.success("Terna ML Engine has terminated successfully.")

    def add_pipeline(self, name):
        """
        Add a new pipeline to the engine.

        @param name: name of the pipeline
        @return: the created pipeline
        """

        # Initialize the pipeline
        p = Pipeline(name=name, logger=self.logger, storage_manager=self.storage_manager)

        # Add the pipeline to the list to be executed
        self.pipelines.append(p)

        self.logger.info("Pipeline '{}' added to the engine".format(p.pipeline_name))

        # Return the pipeline
        return p

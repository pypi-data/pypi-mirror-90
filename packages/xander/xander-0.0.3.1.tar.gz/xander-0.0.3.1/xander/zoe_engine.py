import json

from xander.engine.client import ZoeClient
from xander.engine.pipeline import Pipeline
from xander.engine.storage_manager import StorageManager
from xander.utils.logger import ZoeLogger


class ZoeEngine:
    """
    The core of ZOE ML OPS tool.
    It is the entry point for the user.
    """

    def __init__(self, local_source, local_destination, api_auth_file='zoe_sapphire.json'):
        """
        Class constructor.

        :param local_source: source folder in the local device
        :param local_destination: destination folder in the local device
        :param api_auth_file: authentication file to connect to cloud server
        """

        # Initialize the log manager
        self.logger = ZoeLogger(project_name="Terna")
        self.client = None

        self.logger.success('Zoe ML Engine is ready.')

        try:
            api_auth_file = json.load(open(api_auth_file, 'r'))
            self.client = ZoeClient(api=api_auth_file, logger=self.logger)

            self.logger.info('Cloud mode is active.')
        except:
            self.logger.info('Local mode is active, API auth file not found!')

        self.storage_manager = StorageManager(local_source=local_source, local_destination=local_destination,
                                              logger=self.logger)

        self.pipelines = []

    def run(self):
        self.logger.success("Terna ML Engine is running.")

        for i, pipeline in enumerate(self.pipelines):
            self.logger.info("({}/{}) Running '{}'".format(i + 1, len(self.pipelines), pipeline.pipeline_slug))
            pipeline.run()
            self.logger.info("Completed '{}'.".format(pipeline.pipeline_slug))

        self.logger.success("Terna ML Engine has terminated successfully.")

    def add_pipeline(self, name):
        p = Pipeline(name=name, logger=self.logger, storage_manager=self.storage_manager)
        self.pipelines.append(p)

        self.logger.info("Pipeline '{}' added to the engine".format(p.pipeline_name))

        return p

from feedoo.pipeline_mp import PipelineMP
from feedoo.plugins import Plugins
from feedoo.feedoo_states import FeedooStates
from feedoo.privileges import Privileges
import time
import sys
import logging
import os


class FeedManager:
    def __init__(self, configuration):
        self._configuration = configuration
        self._pipelines = []
        self._log = logging.getLogger(str(self.__class__.__name__))
        self._states = None
        self._privileges = Privileges(*self._configuration.get_privileges())

    def setup(self):
        plugins = Plugins()
        action_modules = plugins.load_vanilla()
        action_modules.update(plugins.load_addons())
        self._privileges.decrease_privileges()
        for pipeline_id, pipeline_actions in self._configuration.iterate_pipelines():
            self._log.info("Create pipeline {}".format(pipeline_id))
            new_pipeline = PipelineMP(action_modules, self._privileges)
            new_pipeline.create(pipeline_id, pipeline_actions)

            self._pipelines.append(new_pipeline)

        self.setup_states()

    def setup_states(self):
        parameters = self._configuration.get_states_parameters()
        parameters["callback"] = self.get_states
        self._states = FeedooStates(**parameters)

    def drop_privileges(self):
        self._privileges.drop_privileges()

    def update(self):
        output = False
        for p in self._pipelines:
            output |= p.update()
        return output

    def finish(self):
        self._log.debug("Call finish()")
        for p in self._pipelines:
            p.finish()
        self._states.finish()

    def loop(self):
        try:
            self._log.debug("Start processing")
            while(1):
                changed = self.update()
                if changed == False:
                    time.sleep(0.25)
        except KeyboardInterrupt:
            self.finish()
            sys.exit(0)

    def get_states(self):
        pipeline_states = dict([p.get_states() for p in self._pipelines])
        timestamp = time.time()

        return {
            "timestamp" : timestamp,
            "pipelines" : pipeline_states
        }

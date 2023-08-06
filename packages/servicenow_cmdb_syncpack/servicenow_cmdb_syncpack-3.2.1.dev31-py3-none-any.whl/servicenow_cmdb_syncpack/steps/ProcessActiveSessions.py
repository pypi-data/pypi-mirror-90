import os

from ipaascommon.content_manger import IpaasContentManager
from ipaascore.BaseStep import BaseStep
from servicenow_base_syncpack.util.snow_parameters import region_param
from couchbase.exceptions import NotFoundError


class ProcessActiveSessions(BaseStep):
    def __init__(self):
        self.friendly_name = "Process Active Discovery Sessions"
        self.description = "Compares active Discovery Sessions to cached list."
        self.version = "3.0.1"

        self.add_step_parameter_from_object(region_param)

    def execute(self):
        cached_sessions_result = self.get_data_from_step_by_name(
            "Load Created Sessions from Cache"
        )
        active_sessions = self.get_data_from_step_by_name(
            "Pull Active Discovery Sessions from ScienceLogic"
        )
        region = self.get_parameter(region_param.name)

        self.logger.flow("Pulled {} active sessions.".format(len(active_sessions)))
        self.logger.debug("Active Sessions: {}".format(active_sessions))

        if cached_sessions_result:
            if type(cached_sessions_result) is dict:
                cached_sessions = [cached_sessions_result]
            else:
                cached_sessions = cached_sessions_result
        else:
            cached_sessions = []

        self.logger.flow("Pulled {} cached sessions.".format(len(cached_sessions)))
        self.logger.debug("Cached Sessions: {}".format(cached_sessions))
        cmanager = IpaasContentManager()

        sessions = []
        for cached_session in cached_sessions:
            slid = os.path.basename(cached_session["location"])
            active_match = [
                x
                for x in active_sessions
                if x["AA__key_val__"] == cached_session["location"]
            ]
            sessions.append(
                {
                    "sys_id": cached_session["sys_id"],
                    "uri": f"/api/discovery_session/{slid}/log?extended_fetch=1",
                    "slid": slid,
                    "affected_cis": cached_session["affected_cis"],
                }
            )
            if not active_match:
                key_to_del = 'disco_session_{}_{}_{}'.format(
                    region, cached_session["sys_id"], slid)
                try:
                    cmanager.delete_from_logs_bucket(key_to_del)
                    self.logger.debug("Removed old discovery "
                                      "session from cache: {}"
                                      .format(key_to_del))
                except NotFoundError:
                    self.logger.debug("{} not deleted as it was not found."
                                      .format(key_to_del))
                except Exception as e:
                    self.logger.error("Encountered error trying to "
                                      "delete old cache entry: {}."
                                      "Error was: {}".format(key_to_del,
                                                             repr(e)))
        self.logger.flow(
            "Pulling logs for {} discovery sessions.".format(len(sessions))
        )
        self.logger.debug("Sessions: {}".format(sessions))

        self.save_data_for_next_step(sessions)

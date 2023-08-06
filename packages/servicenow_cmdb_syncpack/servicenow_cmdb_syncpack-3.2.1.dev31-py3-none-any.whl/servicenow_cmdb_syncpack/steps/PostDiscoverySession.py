import os

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon import ipaas_exceptions
from ipaascommon.content_manger import IpaasContentManager
from servicenow_base_syncpack.util.snow_parameters import region_param
from servicenow_cmdb_syncpack.util.cmdb_params import (
    affected_ci_param,
    service_request_failed_param,
    service_request_in_progress_param,
    service_request_sys_id_param,
)


class PostDiscoverySession(QueryREST):
    def __init__(self):
        super(PostDiscoverySession, self).__init__()
        self.friendly_name = "Post Discovery Session"
        self.description = (
            "Post Discovery Session to ScienceLogic and Prep Callback to ServiceNow"
        )
        self.version = "3.0.0"
        self.add_step_parameter_from_object(service_request_sys_id_param)
        self.add_step_parameter_from_object(service_request_in_progress_param)
        self.add_step_parameter_from_object(service_request_failed_param)
        self.add_step_parameter_from_object(affected_ci_param)
        self.add_step_parameter_from_object(region_param)

    def get_snow_payload(self, sys_id, update, state=None):
        """
        Process SL1 response for ServiceNow callback.
        Args:
            sys_id (str): sys_id of target record.
            update (str): update to send to target record.
            state (str): target record state.

        Returns: formatted payload.

        """
        payload = {"request": sys_id, "work_notes": update}
        if state:
            payload["request_state"] = state

        snow_payload = {"records": [payload]}
        self.logger.debug("Snow Payload: {}".format(snow_payload))
        return snow_payload

    def execute(self):
        state = ""
        update = ""
        sys_id = self.get_parameter(service_request_sys_id_param.name)
        in_progress_state = self.get_parameter(service_request_in_progress_param.name)
        failed_state = self.get_parameter(service_request_failed_param.name)
        region = self.get_parameter(region_param.name)

        try:
            super(PostDiscoverySession, self).execute()
        except ipaas_exceptions.StepFailedException as e:
            response = self.get_current_saved_data()
            if response:
                error = (
                    f"HTTP code {response['http_code']} received when posting to SL1."
                )
                debug = (
                    f"HTTP Code: {response['http_code']}, "
                    f"Headers: {response['headers']}, "
                    f"Body: {response['body']}"
                )
            else:
                error = "Post to SL1 Failed"
                debug = e
            self.logger.error(error)
            self.logger.debug(debug)
            state = failed_state
            update = (
                f"Create Discovery Session Failed while posting to SL1. "
                f"Details: {debug}"
            )
        else:
            em7_response = self.get_current_saved_data()
            self.logger.debug(em7_response)

            self.logger.info(f"Discovery Session URI: {em7_response.get('location')}")
            affected_cis = self.get_parameter(affected_ci_param.name)
            slid = os.path.basename(em7_response.get("location"))
            update = f"Discovery Session {slid} Started in ScienceLogic"
            state = in_progress_state
            cmanager = IpaasContentManager()
            cmanager.save_to_cache(
                f"disco_session_{region}_{sys_id}_{slid}",
                {
                    "location": em7_response.get("location"),
                    "sys_id": sys_id,
                    "affected_cis": affected_cis,
                },
            )
        finally:
            snow_payload = self.get_snow_payload(sys_id, update, state)

            self.save_data_for_next_step(snow_payload)

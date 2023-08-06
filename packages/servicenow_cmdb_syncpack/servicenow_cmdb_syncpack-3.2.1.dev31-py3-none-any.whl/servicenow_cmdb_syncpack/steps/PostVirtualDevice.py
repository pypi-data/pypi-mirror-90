import os

from ipaascommon import ipaas_exceptions

from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_cmdb_syncpack.util.cmdb_params import (
    service_request_success_param,
    service_request_failed_param,
    service_request_sys_id_param,
)


class PostVirtualDevice(QueryREST):
    def __init__(self):
        super(PostVirtualDevice, self).__init__()
        self.friendly_name = "Post Virtual Device"
        self.description = (
            "Post Virtual Device to ScienceLogic and Prep " "Callback to ServiceNow"
        )
        self.version = "2.0.2"
        self.add_step_parameter_from_object(service_request_sys_id_param)
        self.add_step_parameter_from_object(service_request_success_param)
        self.add_step_parameter_from_object(service_request_failed_param)

    def execute(self):
        success_state = self.get_parameter(service_request_success_param.name)
        failed_state = self.get_parameter(service_request_failed_param.name)
        state = ""
        update = ""
        try:
            super(PostVirtualDevice, self).execute()
        except ipaas_exceptions.StepFailedException as err:
            response = self.get_current_saved_data()
            if response:
                error = "HTTP code {} received when posting to SL1.".format(
                    response["http_code"]
                )
                debug = "HTTP Code: {}, Headers: {}, Body: {}".format(
                    response["http_code"], response["headers"], response["body"]
                )
            else:
                error = "Post to SL1 Failed"
                debug = err
            self.logger.error(error)
            self.logger.debug(debug)
            state = failed_state
            update = (
                "Create Virtual Device Failed while posting to SL1. "
                "Details: {}".format(debug)
            )
        else:
            sl1_response = self.get_current_saved_data()
            self.logger.debug(sl1_response)

            if sl1_response:
                slid = os.path.basename(sl1_response.get("location"))
                update = "Virtual Device {} created with SLID: {}".format(
                    sl1_response.get("name"), slid
                )
                state = success_state
        finally:
            sys_id = self.get_parameter(service_request_sys_id_param.name)
            payload = {"request": sys_id, "work_notes": update, "request_state": state}
            snow_payload = {"records": [payload]}
            self.logger.debug(u"Snow Payload: {}".format(snow_payload))
            self.save_data_for_next_step(snow_payload)

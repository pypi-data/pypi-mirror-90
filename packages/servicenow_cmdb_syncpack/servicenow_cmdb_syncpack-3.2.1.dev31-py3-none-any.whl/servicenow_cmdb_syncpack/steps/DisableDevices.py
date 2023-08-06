from ipaascommon import ipaas_exceptions
from ipaascore import parameter_types

from base_steps_syncpack.steps.QueryGQL import QueryGQL
from servicenow_cmdb_syncpack.util.cmdb_params import (
    service_request_success_param,
    service_request_failed_param,
    service_request_sys_id_param,
)


class DisableDevices(QueryGQL):
    def __init__(self):
        super(DisableDevices, self).__init__()
        self.friendly_name = "Disable Devices in SL1"
        self.description = (
            "Disables Devices in SL1 by moving them to a Virtual Collector Group"
        )
        self.version = "1.0.0"
        self.add_step_parameter_from_object(service_request_sys_id_param)
        self.add_step_parameter_from_object(service_request_success_param)
        self.add_step_parameter_from_object(service_request_failed_param)
        self.new_step_parameter(
            name="final_state",
            description="Final Ticket state from Verify step.",
            param_type=parameter_types.NumberParameter(),
        )
        self.new_step_parameter(name="devices")

    def execute(self):
        failed_state = self.get_parameter(service_request_failed_param.name)
        state = ""
        update = ""
        devices = self.get_parameter("devices", None)
        sys_id = self.get_parameter(service_request_sys_id_param.name)

        if devices:
            self.logger.flow(
                "Disabling {} devices. DIDs: {}".format(len(devices), devices)
            )
            try:
                super(DisableDevices, self).execute()
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
                update = "Disabling Devices Failed while posting to SL1. Details: {}".format(
                    debug
                )
            else:
                final_state = int(self.get_parameter("final_state", None))
                sl1_response = self.get_current_saved_data()
                self.logger.debug(sl1_response)

                if sl1_response:
                    result = sl1_response.get("updateDevices", list())
                else:
                    result = list()
                if result:
                    cug = result[0].get("collectorGroup", dict())
                    dids = [x["id"] for x in result]
                    update = "Successfully Moved DIDs {} to Collector Group: {} (ID: {})".format(
                        dids, cug.get("name"), cug.get("id")
                    )
                    state = final_state
                else:
                    update = "No devices updated"
                    state = failed_state
            finally:
                self.logger.flow(update)
                payload = {
                    "request": sys_id,
                    "work_notes": update,
                    "request_state": state,
                }
                snow_payload = {"records": [payload]}
                self.logger.debug(u"Snow Payload: {}".format(snow_payload))
                self.save_data_for_next_step(snow_payload)
        else:
            self.logger.flow("No devices to disable. Skipping.")
            self.save_data_for_next_step(
                {
                    "records": [
                        {
                            "request": sys_id,
                            "work_notes": "No devices found to disable in SL1.",
                            "request_state": failed_state,
                        }
                    ]
                }
            )

import json

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.ipaas_exceptions import StepFailedException
from ipaascommon.ipaas_utils import str_to_bool  # INT-1056
from ipaascore.parameter_types import BoolParameterToggle, StringParameterShort
from servicenow_cmdb_syncpack.util.cmdb_params import domain_sep_param


class PostCIsToSnow(QueryREST):
    def __init__(self):
        super(PostCIsToSnow, self).__init__()
        self.friendly_name = "Post CIs to ServiceNow"
        self.description = "Posts CI payloads to ServiceNow"
        self.version = "1.1.1"
        self.new_step_parameter(
            name="Simulation_Mode",
            description="Enable Simulation Mode on ServiceNow Identification Engine.\nWill return results without changing ServiceNow CMDB",
            default_value=False,
            required=False,
            param_type=BoolParameterToggle(),
        )
        self.add_step_parameter_from_object(domain_sep_param)

        del self.parameters["relative_url"]  # unset default
        self.new_step_parameter(name="relative_url", param_type=StringParameterShort())

    def execute(self):
        domain_sep_enabled = str_to_bool(self.get_parameter(domain_sep_param.name))
        simulation_mode = self.get_parameter("Simulation_Mode").lower()

        rel_url = self.parameters.get("relative_url")

        if domain_sep_enabled:
            rel_url.value = "/api/10693/sciencelogic_domain_separation/IdentificationEngine?test={}".format(
                simulation_mode
            )
        else:
            rel_url.value = "/api/x_sclo_scilogic/v1/sciencelogic/IdentificationEngine?test={}".format(
                simulation_mode
            )

        self.logger.flow("Posting to relative_url: {}".format(rel_url.value))
        self.logger.info(
            "Post payload: {}".format(json.dumps(self.get_parameter("payload")))
        )

        super(PostCIsToSnow, self).execute()
        snow_response = self.get_current_saved_data()
        self.logger.info("ServiceNow Result: {}".format(json.dumps(snow_response)))

        ident_results = {
            "created": set(),
            "updated": set(),
            "skipped": set(),
            "error": set(),
        }
        snow_to_bucket = {
            "INSERT": "created",
            "UPDATE": "updated",
            "UPDATE_WITH_UPGRADE": "updated",
            "UPDATE_WITH_DOWNGRADE": "updated",
            "UPDATE_WITH_SWITCH": "updated",
            "NO_CHANGE": "skipped",
            "ERROR": "error",
        }
        for block in snow_response["result"]:
            if "input_payload" not in block:
                if domain_sep_enabled:
                    sub_message = (
                        "Ensure Domain Separation Update Set version 3.0+ is installed"
                    )
                else:
                    sub_message = "Ensure ServiceNow App version 1.0.33+ is Installed."
                raise StepFailedException(
                    f"Invalid Response received from ServiceNow. {sub_message}"
                )
            input_items = block["input_payload"]["items"]
            response_items = block["response"]["items"]
            for in_payload, response in zip(input_items, response_items):
                ro = Response(in_payload, response)
                ident_results[snow_to_bucket[ro.operation]].add(ro)

        self.logger.flow(
            "Simulation Mode: {}\n Result: {} Created, {} Updated, {} Skipped, {} Errors".format(
                simulation_mode,
                len(ident_results["created"]),
                len(ident_results["updated"]),
                len(ident_results["skipped"]),
                len(ident_results["error"]),
            )
        )
        self.logger.info(
            "Created: {}\n Updated: {}\n Skipped: {}".format(
                [x.__dict__() for x in ident_results["created"]],
                [x.__dict__() for x in ident_results["updated"]],
                [x.__dict__() for x in ident_results["skipped"]],
            )
        )
        if ident_results["error"]:
            errors = list()
            for error in list(ident_results["error"]):
                errors.append(
                    {"error": error.__dict__(), "input_payload": error.input_payload}
                )
            self.logger.warning(f"Errors Received from ServiceNow.\nErrors: {errors}")
        self.save_data_for_next_step([])


class Response(object):
    def __init__(self, input_payload, response_payload):
        """
        Instantiates Response Object from ServiceNow Result

        Args:
            input_payload (dict): Input Payload sent to ServiceNow
            response_payload (dict): Response received from ServiceNow
        """
        self.input_payload = input_payload
        self.response_payload = response_payload
        self.identification_attempt = self.get_identification_attempt()
        self.errors = self.get_errors()
        self.sl1_id = self.input_payload["values"].get("x_sclo_scilogic_id")
        self.name = self.input_payload["values"].get("name")
        self.sys_id = self.response_payload.get("sysId")
        self.ci_class = self.response_payload.get("className")
        self.operation = self.response_payload.get("operation", "ERROR")
        self.identifierEntrySysId = self.response_payload.get("identifierEntrySysId")

    def __str__(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "sl1_id": self.sl1_id,
            "name": self.name,
            "sys_id": self.sys_id,
            "ci_class": self.ci_class,
            "operation": self.operation,
            "identifierEntrySysId": self.identifierEntrySysId,
            "ident_attempt": self.identification_attempt,
            "errors": self.errors,
        }

    def get_identification_attempt(self):
        try:
            ident_attempt_dict = next(
                iter(
                    [
                        x
                        for x in self.response_payload.get(
                            "identificationAttempts", list()
                        )
                        if x["attemptResult"] == "MATCHED"
                    ]
                )
            )
        except StopIteration:
            ident_attempt = None
        else:
            ident_attempt = {
                "name": ident_attempt_dict.get("identifierName"),
                "result": ident_attempt_dict.get("attemptResult"),
                "attributes": ident_attempt_dict.get("attributes", list()),
                "hybridEntryCiAttributes": ident_attempt_dict.get(
                    "hybridEntryCiAttributes", list()
                ),
                "searchOnTable": ident_attempt_dict.get("searchOnTable"),
            }
        return ident_attempt

    def get_errors(self):
        errors = self.response_payload.get("errors", list())

        return errors if errors else None

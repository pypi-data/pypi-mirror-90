import urllib.parse
from os.path import basename
from typing import Dict, List, Union

from base_steps_syncpack.steps.QueryREST import OBJECT_KEY_VAL, QueryREST
from ipaascore.parameter_types import StringParameterShort
from isbaseutils.utils import str_to_bool
from servicenow_base_syncpack.util.helpers import add_to_payload_if_not_empty
from servicenow_base_syncpack.util.snow_parameters import chunk_size_param, region_param


class PullAndProcessDiscoverySessions(QueryREST):
    def __init__(self):
        super(PullAndProcessDiscoverySessions, self).__init__()

        self.friendly_name = "Pull and Process Discovery Sessions"
        self.description = (
            "Pulls and Processes Discovery Sessions from SL1 and generates Discovery "
            "Templates for ServiceNow."
        )
        self.version = "1.0.0"

        self.add_step_parameter_from_object(region_param)

        self.new_step_parameter(
            name="template_prefix",
            description="Name Prefix that designates Discovery Templates in SL1",
            sample_value="ServiceNow Template:",
            default_value="ServiceNow Template:",
            required=True,
            param_type=StringParameterShort(),
        )
        del self.parameters["relative_url"]  # unset default
        self.new_step_parameter(name="relative_url", param_type=StringParameterShort())

        self.prefix = str()

    def process_sessions(self) -> List[Dict[str, Union[str, bool, List[str]]]]:
        region = self.get_parameter(region_param.name)

        discovery_sessions = self.get_current_saved_data()

        templates = list()
        drop_fields = [
            "date_edit",
            "edited_by",
            "date_run",
            "ip_lists",
            "hostnames",
            "logs",
            "duplicate_protection",
            "model_override",
        ]
        bool_fields = [
            "discover_non_snmp",
            "model_device",
            "dhcp_enabled",
            "log_all",
            "bypass_interface_inventory",
        ]
        for session in discovery_sessions:
            if self.prefix in session.get("name"):
                template = {"region": region}
                for key, value in session.items():
                    if key == OBJECT_KEY_VAL:
                        key = "id"
                    if key in drop_fields:
                        continue
                    elif key in ["credentials", "device_groups"]:
                        if key:
                            add_to_payload_if_not_empty(
                                ",".join([basename(x) for x in value]), key, template
                            )
                        else:
                            continue
                    elif key in bool_fields:
                        add_to_payload_if_not_empty(str_to_bool(value), key, template)
                    elif value:
                        if "/api" in value:
                            add_to_payload_if_not_empty(basename(value), key, template)
                        elif isinstance(value, list):
                            add_to_payload_if_not_empty(",".join(value), key, template)
                        else:
                            add_to_payload_if_not_empty(value, key, template)
                    else:
                        continue
                templates.append(template)
        return templates

    def chunk_for_snow(self, templates: List[dict]) -> List[Dict[str, Dict[str, list]]]:
        """
        Chunk Payloads for ServiceNow.

        Args:
            templates: List of Templates

        Returns:

        """
        chunk_size = int(self.get_parameter(chunk_size_param.name))

        self.logger.flow(f"Found {len(templates)} templates to send to ServiceNow")
        loop_list = {"records": []}
        chunked_payloads = []
        count = 0
        for payload in templates:
            if count + 1 <= chunk_size:
                loop_list["records"].append(payload)
            else:
                chunked_payloads.append({"payload": loop_list})
                loop_list = {"records": []}
                count = 0
                loop_list["records"].append(payload)
            count += 1
        if loop_list:
            chunked_payloads.append({"payload": loop_list})

        self.logger.flow("Sending {} Chunks".format(len(chunked_payloads)))
        self.logger.debug("Chunks: {}".format(chunked_payloads))

        return chunked_payloads

    def execute(self):
        rel_url = self.parameters.get("relative_url")
        self.prefix = self.get_parameter("template_prefix")

        rel_url.value = (
            f"/api/discovery_session?extended_fetch=1&"
            f"filter.0.name.begins_with={urllib.parse.quote(self.prefix)}"
        )

        super(PullAndProcessDiscoverySessions, self).execute()
        chunked_payloads = self.chunk_for_snow(self.process_sessions())
        self.save_data_for_next_step(chunked_payloads)

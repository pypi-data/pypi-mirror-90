# noinspection PyCompatibility
from typing import Tuple
import ipaddress
import json
import re

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.ipaas_utils import str_to_bool
from ipaascore import parameter_types
from servicenow_base_syncpack.util.helpers import add_to_payload_if_not_empty
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullAndProcessServiceRequests(QueryREST):
    def __init__(self):
        super(PullAndProcessServiceRequests, self).__init__()
        self.friendly_name = "Pull and Process Service Requests"
        self.description = "Processes pulled service requests to send to ScienceLogic"
        self.version = "3.0.0"
        self.add_step_parameter_from_object(region_param)
        self.new_step_parameter(
            name="Open_State",
            description="State for Open Requests.",
            sample_value=3,
            default_value=1,
            required=True,
            param_type=parameter_types.NumberParameter(),
        )

    @staticmethod
    def bool_to_int(test_var):
        """
        Convert bool Str to 0/1.
        Args:
            test_var (str): Variable to Convert

        Returns (str): 0/1/None

        """
        if (
            not test_var
            or test_var == "System Default (Recommended)"
        ):
            return None
        elif isinstance(test_var, str):
            if test_var.lower() == "default":
                return None

        var_bool = str_to_bool(test_var)
        if var_bool:
            return "1"
        else:
            return "0"

    def parse_sources(self, sources: str) -> Tuple[list, list]:
        """
        Convert comma separated string of hosts/ips to lists.
        Source can be a mix of types and need to be split out and converted.
        Args:
            sources (str): Comma Separated string of values.

        Returns: Tuple of Lists of Ip Ranges / Hostnames.

        """
        ip_lists = []
        hostnames = []
        ip_range_search = re.compile(
            r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s*-"
            r"\s*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        )

        sources_list = sources.split(",")
        for source in sources_list:
            s = source.strip()
            if ip_range_search.search(s):  # Is IP range?
                ip_range = s.split(" - ")
                ip_lists.append(
                    {"start_ip": ip_range[0].strip(), "end_ip": ip_range[1].strip()}
                )
            else:
                try:
                    ipaddress.ip_address(s)  # Is IP Address?
                except (ipaddress.AddressValueError, ValueError):
                    try:
                        ipaddress.ip_network(s)  # Is CIDR?
                    except (ipaddress.AddressValueError, ValueError):
                        hostnames.append(s)
                    else:
                        hosts = list(ipaddress.ip_network(s).hosts())
                        if hosts:
                            ip_lists.append(
                                {"start_ip": str(hosts[0]), "end_ip": str(hosts[-1])}
                            )
                        else:
                            self.logger.warning(
                                "Invalid ip_network received, Ignoring."
                            )
                            continue
                else:
                    ip_lists.append({"start_ip": s, "end_ip": s})

        return ip_lists, hostnames

    def process_disco_session(self, disco_session: dict):
        """
        Convert list of SNOW discovery dictionaries to SL1 Payloads.
        Args:
            disco_session (dict): Discovery dictionaries from SNOW.

        Returns: Formatted SL1 payload.

        """

        ip_lists, hostnames = self.parse_sources(
            disco_session.get("ip_hostname_list", "")
        )
        payload = {
            "name": disco_session.get("number", ""),
            "description": "Created by ServiceNow Request Number: {}".format(
                disco_session.get("number", "")
            ),
            "organization": "/api/organization/{}".format(
                disco_session.get("organization", "")
            ),
            "aligned_collector": "/api/appliance/{}".format(
                disco_session.get("collection_server", "")
            ),
        }
        add_to_payload_if_not_empty(
            disco_session.get("scan_ports", "").split(","), "scan_ports", payload
        )
        add_to_payload_if_not_empty(
            self.bool_to_int(disco_session.get("dhcp")), "dhcp_enabled", payload
        )
        add_to_payload_if_not_empty(
            self.bool_to_int(disco_session.get("discover_non_snmp")),
            "discover_non_snmp",
            payload,
        )
        add_to_payload_if_not_empty(
            self.bool_to_int(disco_session.get("model_devices")),
            "model_device",
            payload,
        )
        add_to_payload_if_not_empty(
            self.bool_to_int(disco_session.get("log_all")), "log_all", payload
        )
        add_to_payload_if_not_empty(
            self.bool_to_int(disco_session.get("bypass_interface_inventory")),
            "bypass_interface_inventory",
            payload,
        )
        add_to_payload_if_not_empty(
            disco_session.get("maximum_allowed_interfaces", 0),
            "max_interface_inventory_count",
            payload,
        )
        add_to_payload_if_not_empty(
            disco_session.get("interface_inventory_timeout", 0),
            "interface_inventory_timeout",
            payload,
        )
        add_to_payload_if_not_empty(
            disco_session.get("device_model_cache_ttl_h", 0), "pre_device_ttl", payload
        )
        add_to_payload_if_not_empty(ip_lists, "ip_lists", payload)
        add_to_payload_if_not_empty(hostnames, "hostnames", payload)

        template = disco_session.get("device_template", None)
        if template:
            payload["aligned_device_template"] = "/api/device_template/{}".format(
                template
            )
        if disco_session.get("initial_scan_level") != "System Default (Recommended)":
            payload["initial_scan_level"] = disco_session.get("initial_scan_level")
        scan_all_ips = self.bool_to_int(disco_session.get("port_scan_all"))
        if scan_all_ips:
            payload["scan_all_ips"] = scan_all_ips
        if disco_session.get("port_scan_timeout") != "System Default (Recommended)":
            payload["port_scan_timeout"] = disco_session.get("port_scan_timeout")
        if disco_session.get("scan_throttle") != "System Default (Recommended)":
            payload["scan_throttle"] = disco_session["scan_throttle"]

        if disco_session.get("credentials", None):
            credentials = list()
            for credential in disco_session.get("credentials", []):
                cat = credential["Category"].split("Credentials")[0].lower()
                credentials.append(f"/api/credential/{cat}/{credential['ID']}")
            add_to_payload_if_not_empty(credentials, "credentials", payload)
        if disco_session.get("add_devices_to_device_groups", None):
            device_groups = list()
            for device_group in disco_session["add_devices_to_device_groups"]:
                device_groups.append(
                    "/api/device_group/{}".format(device_group["SL1 ID"].strip())
                )
            add_to_payload_if_not_empty(device_groups, "device_groups", payload)

        return {
            "payload": payload,
            "sys_id": disco_session.get("sysid", ""),
            "affected_cis": disco_session.get("affected"),
        }

    @staticmethod
    def process_virtual_device(virtual_device):
        """
        Convert SNOW Virtual Device Create request to SL1 Payload.
        Args:
            virtual_device (dict): SNOW payload.

        Returns: converted payload.

        """
        payload = {
            "organization": "/api/organization/{}".format(
                virtual_device.get("organization", "")
            ),
            "name": virtual_device.get("name", ""),
            "class_type": "/api/device_class/{}".format(
                virtual_device.get("virtual_device_class", "")
            ),
            "collector_group": "/api/collector_group/{}".format(
                virtual_device.get("collector_group", "")
            ),
        }
        return {"payload": payload, "sys_id": virtual_device.get("sysid", "")}

    @staticmethod
    def process_delete_requests(session):
        sys_id = session.get("sysid")
        devices = list()

        for device in session.get("device_monitoring_removal", []):
            devices.append(int(device.get("id", 0)))

        gql_search = {"search": {"id": {"in": devices}}}

        payload = {"sys_id": sys_id, "gql_search": json.dumps(gql_search)}
        return payload

    def execute(self):
        """
        All logic main logic for executing the step happens here
        :return:
        """
        super(PullAndProcessServiceRequests, self).execute()
        snow_requests = self.get_current_saved_data()

        self.logger.flow("Pulled {} Service Requests".format(len(snow_requests)))
        self.logger.debug("snow_sessions: {}".format(snow_requests))

        sl1_payloads = {
            "disco_sessions": list(),
            "virtual_device_creates": list(),
            "device_deletes": list(),
        }
        for session in snow_requests:
            if session["request_type"] == "discover_device":
                sl1_payloads["disco_sessions"].append(
                    self.process_disco_session(session)
                )
            elif session["request_type"] == "create_virtual_device":
                sl1_payloads["virtual_device_creates"].append(
                    self.process_virtual_device(session)
                )
            elif session["request_type"] == "remove_device":
                sl1_payloads["device_deletes"].append(
                    self.process_delete_requests(session)
                )

        self.logger.debug("SL1 Payloads: {}".format(sl1_payloads))
        self.save_data_for_next_step(sl1_payloads)

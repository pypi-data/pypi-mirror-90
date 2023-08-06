from datetime import datetime
from os.path import basename
from typing import Optional, Tuple

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascommon.content_manger import IpaasContentManager
from ipaascommon.ipaas_utils import str_to_bool
from ipaascore.parameter_types import StringParameterShort
from servicenow_base_syncpack.util.snow_parameters import region_param
from servicenow_cmdb_syncpack.util.cmdb_params import (
    affected_ci_param,
    service_request_success_param,
    service_request_sys_id_param,
)
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullDiscoverySessionLogs(QueryREST):
    def __init__(self):
        self.add_step_parameter_from_object(region_param)
        super(PullDiscoverySessionLogs, self).__init__()
        self.friendly_name = "Pull Discovery Session Logs"
        self.description = (
            "Pull Discovery Session Logs from ScienceLogic and "
            "prepare updates for ServiceNow"
        )
        self.version = "3.0.0"
        self.add_step_parameter_from_object(service_request_sys_id_param)
        self.add_step_parameter_from_object(service_request_success_param)
        self.add_step_parameter_from_object(affected_ci_param)

        self.new_step_parameter(
            name="sys_id_target",
            description="Target field in SL1 for ServiceNow CI sys_id",
            required=False,
            default_value=str(),
            sample_value="c-sys_id",
            param_type=StringParameterShort(),
        )
        self.new_step_parameter(
            name="ci_class_target",
            description="Target field in SL1 for ServiceNow CI Class Type",
            required=False,
            default_value=str(),
            sample_value="c-ci_class_target",
            param_type=StringParameterShort(),
        )

        self.sys_id = str()
        self.success_state = str()
        self.affected_cis = dict()
        self.sys_id_target = None
        self.ci_class_target = None
        self.region = None

    def get_sl1_payload(self, log: dict) -> Optional[dict]:
        if self.sys_id_target or self.ci_class_target:
            affected_ci = self.affected_cis.get(
                log["ip"].split(" (*IP)")[0].strip(), dict()
            )
            payload = dict()
            if self.sys_id_target and affected_ci.get("sys_id"):
                payload[
                    self.sys_id_target
                    if self.sys_id_target.startswith("c-")
                    else f"c-{self.sys_id_target}"
                ] = affected_ci["sys_id"]
            if self.ci_class_target and affected_ci.get("class"):
                payload[
                    self.ci_class_target
                    if self.ci_class_target.startswith("c-")
                    else f"c-{self.ci_class_target}"
                ] = affected_ci["class"]
            if payload:
                return {"did": basename(log["device"]), "payload": payload}
        return None

    def process_log(
        self, log: dict, cached_timestamp: Optional[int]
    ) -> Tuple[Optional[dict], float, str, Optional[dict]]:
        """
        Process SL1 Log and convert to SNOW Update.
        Args:
            log (dict): Log Record to parse.
            cached_timestamp (int): Last timestamp processed during last run.

        Returns: SNOW Update

        """
        state = ""
        discovery_id = log.get("discovery_id")
        sl1_payload = None
        if cached_timestamp and float(log["log_stamp"]) <= cached_timestamp:
            return None, 0, discovery_id, sl1_payload

        log_time = datetime.utcfromtimestamp(float(log["log_stamp"])).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if "Discovered and modeled" in log["msg_txt"]:
            update = (
                "{} | Discovery Session: {} | {} | IP: {} | Name: {} | "
                "SL_ID: {}".format(
                    log_time,
                    discovery_id,
                    log["msg_txt"],
                    log["ip"],
                    log["name"],
                    basename(log["device"]),
                )
            )
            sl1_payload = self.get_sl1_payload(log)
        elif log.get("ip", None):
            update = (
                "{} | Discovery Session: {} | {} | IP: {} | Name: {} | "
                "found: {} | managable: {}".format(
                    log_time,
                    discovery_id,
                    log["msg_txt"],
                    log["ip"],
                    log["name"],
                    str_to_bool(log["found"]),
                    str_to_bool(log["managable"]),
                )
            )
            sl1_payload = self.get_sl1_payload(log)

        elif log["msg_id"] == "125":
            update = "{} | Discovery Session: {} | {}".format(
                log_time, discovery_id, log["msg_txt"]
            )
            state = self.success_state
        else:
            update = "{} | Discovery Session: {} | {}".format(
                log_time, discovery_id, log["msg_txt"]
            )
        snow_payload = {"request": self.sys_id, "work_notes": update}
        if state:
            snow_payload["request_state"] = state
        return snow_payload, float(log["log_stamp"]), discovery_id, sl1_payload

    def execute(self):
        self.sys_id_target = self.get_parameter("sys_id_target")
        self.ci_class_target = self.get_parameter("ci_class_target")
        self.sys_id = self.get_parameter(service_request_sys_id_param.name)
        raw_affected_cis = self.get_parameter(affected_ci_param.name)
        for affected_ci in raw_affected_cis:
            if affected_ci.get("ip_address"):
                self.affected_cis[affected_ci["ip_address"]] = affected_ci

        cache = self.get_data_from_step_by_name(
            "Load Last Processed Log Timestamp from Cache"
        )
        self.success_state = self.get_parameter(service_request_success_param.name)

        if cache:
            cached_timestamp = cache.get("cached_timestamp", None)
        else:
            cached_timestamp = None

        super(PullDiscoverySessionLogs, self).execute()
        if not self.region:
            self.region = self.get_parameter(region_param.name)
        sl1_response = self.get_current_saved_data()
        self.logger.debug("SL1 Response: {}".format(sl1_response))
        max_log_stamp = 0
        raw_snow_payloads = list()
        sl1_payloads = list()
        discovery_id = str()
        for log in sl1_response["result_set"].values():
            if not isinstance(log, dict):
                continue
            raw_snow_payload, log_stamp, discovery_id, sl1_payload = self.process_log(
                log, cached_timestamp
            )
            if log_stamp > max_log_stamp:
                max_log_stamp = log_stamp
            if raw_snow_payload:
                raw_snow_payloads.append(raw_snow_payload)
            if sl1_payload:
                sl1_payloads.append(sl1_payload)

        data_to_save = dict()
        if raw_snow_payloads:
            self.logger.flow(f"Posting {len(raw_snow_payloads)} logs to ServiceNow")
            final_snow_payload = {"records": raw_snow_payloads}
            self.logger.debug(f"Snow Payload: {final_snow_payload}")
            cmanager = IpaasContentManager()
            self.logger.debug(f"Max Log Stamp: {max_log_stamp}")
            cmanager.save_to_cache(
                f"discovery_session_logs_{self.region}_{self.sys_id}_{discovery_id}",
                {"cached_timestamp": max_log_stamp},
            )
            data_to_save["snow_payload"] = final_snow_payload

        else:
            self.logger.flow("No logs found to post to ServiceNow.")
            data_to_save["snow_payload"] = dict()

        if sl1_payloads:
            self.logger.flow(f"Updating {len(sl1_payloads)} SL1 Devices.")
            self.logger.debug(f"SL1 Payloads: {sl1_payloads}")
            data_to_save["sl1_payloads"] = sl1_payloads
        else:
            data_to_save["sl1_payloads"] = list()

        self.save_data_for_next_step(data_to_save)

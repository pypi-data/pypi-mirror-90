from datetime import datetime
from urllib.parse import quote

from ipaascommon.report_manager import StandardReport
from ipaascore.BaseStep import BaseStep
from servicenow_cmdb_syncpack.util.cmdb_params import pf_host_param


class ReportMissingMappings(BaseStep):
    def __init__(self):
        super(ReportMissingMappings, self).__init__()
        self.friendly_name = "Mappings reporter"
        self.description = "Generates a report of Missing mappings"
        self.version = "1.0.0"

        self.add_step_parameter_from_object(pf_host_param)

    def execute(self):
        is_host = self.get_parameter(pf_host_param.name)
        dt = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        report_name = f"{dt}"
        delta_mapping_data = self.get_data_from_step_by_name("Process Device Classes")

        if delta_mapping_data["enabled"]:
            report = StandardReport(
                report_name, self.application_name, "tmp section", True
            )
            self.report_mapping(delta_mapping_data, report)
            self.logger.flow(f"Report {report.report_id} Complete.")
            self.logger.flow(f"Link: https://{is_host}/reports/{quote(report.report_id)}")
        else:
            self.logger.flow("Step is Disabled. Returning empty list.")

    @staticmethod
    def report_mapping(delta_info, report):
        is_section_name = "Missing Device Mappings"
        snow_mappings = delta_info["snowMissing"]
        sl1_mappings = delta_info["sl1Missing"]

        report.add_column(
            "ServiceNow to SL1 Missing Mappings",
            data_key=is_section_name,
            column_data=snow_mappings,
        )
        report.add_column(
            "SL1 to ServiceNow Missing Mappings",
            data_key=is_section_name,
            column_data=sl1_mappings,
        )

from base_steps_syncpack.steps.MySqlSelect import MySqlSelect
from servicenow_base_syncpack.util.snow_parameters import chunk_size_param
from servicenow_cmdb_syncpack.util.cmdb_base_utils import chunk_cis


class PullAndProcessSoftwarePackages(MySqlSelect):
    def __init__(self):
        super(PullAndProcessSoftwarePackages, self).__init__()
        self.friendly_name = "Pull And Process Software Packages"
        self.description = "Parse pulled Software Packages from SL1"
        self.version = "1.0.0"

        self.add_step_parameter_from_object(chunk_size_param)

    def execute(self):
        super(PullAndProcessSoftwarePackages, self).execute()
        packages = self.get_current_saved_data()

        chunk_size = int(self.get_parameter(chunk_size_param.name))

        self.logger.debug(u"software packages: {}".format(packages))

        payload = []

        self.logger.info("Building Software Package Payloads.")
        for package in packages:
            if package.get("title"):
                payload.append(
                    {
                        "items": [
                            {
                                "className": "cmdb_ci_spkg",
                                "values": {
                                    "name": package["title"],
                                    "version": "",
                                    "key": u"{}_:::_NULL".format(package["title"]),
                                    "x_sclo_scilogic_monitored": True,
                                },
                            }
                        ]
                    }
                )
            else:
                continue

        self.logger.flow(
            "Sending {} Software Packages to ServiceNow.".format(len(payload))
        )
        chunked_payloads = chunk_cis(payload, chunk_size)
        self.logger.flow("Sending {} Chunks.".format(len(chunked_payloads)))
        self.logger.debug(u"Package Payloads: {}".format(payload))
        self.save_data_for_next_step(chunked_payloads)

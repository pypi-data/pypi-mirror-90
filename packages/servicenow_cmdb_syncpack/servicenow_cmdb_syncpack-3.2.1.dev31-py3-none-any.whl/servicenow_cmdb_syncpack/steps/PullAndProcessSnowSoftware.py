from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullAndProcessSnowSoftware(QueryREST):
    def __init__(self):
        super(PullAndProcessSnowSoftware, self).__init__()
        self.friendly_name = "Pull and Process ServiceNow Software"
        self.description = "Pulls Software from ServiceNow and Processes Result"
        self.version = "1.0.0"

        self.add_step_parameter_from_object(region_param)

    def execute(self):
        super(PullAndProcessSnowSoftware, self).execute()
        software = self.get_current_saved_data()

        self.logger.debug(u"SNOW Software: {}".format(software))

        result = dict()

        for sw in software:
            did_list = list()
            if sw.get("installed_on"):
                for device in sw.get("installed_on"):
                    did_list.append(device.get("id"))
            if sw.get("package_name"):
                result[sw.get("name")] = {"dids": did_list, "sys_id": sw.get("sys_id")}
            else:
                continue

        self.save_data_for_next_step({"results": result})

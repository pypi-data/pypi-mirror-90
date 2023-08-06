import os

from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullAndProcessCollectorGroups(QueryREST):

    def __init__(self):
        super(PullAndProcessCollectorGroups, self).__init__()
        self.friendly_name = "Process Collector Groups"
        self.description = "Parse pulled Collector Group data from SL1."
        self.version = "2.0.0"
        self.add_step_parameter_from_object(region_param)

    def execute(self):
        region = self.get_parameter(region_param.name)
        super(PullAndProcessCollectorGroups, self).execute()
        em7_response = self.get_current_saved_data()
        self.logger.debug(em7_response)

        if em7_response:
            snow_creates = []
            for group in em7_response:
                if len(group['data_collectors']) == 0:
                    self.logger.info("VCUG Detected, Ignoring.")
                    continue
                sl_id = os.path.basename(group['AA__key_val__'])
                snow_dict = {
                    "name": group['cug_name'],
                    "collectors": ','.join(
                            [os.path.basename(x) for x in group[
                                    'data_collectors']]),
                    "id": sl_id,
                    "region": region,
                    "record_type": "collector_group"
                }
                snow_creates.append(snow_dict)

            if snow_creates:
                self.logger.flow(
                    u"Sending {} Collector Groups.".format(len(snow_creates)))
                self.logger.debug(u"snowCreates: {}".format(snow_creates))
                self.save_data_for_next_step(snow_creates)
            else:
                self.logger.flow("No Collector Groups to send.")
                self.save_data_for_next_step([])

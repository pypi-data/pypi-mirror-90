import os

from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullAndProcessCollectors(QueryREST):

    def __init__(self):
        super(PullAndProcessCollectors, self).__init__()
        self.friendly_name = "Process Collectors"
        self.description = "Parse pulled Collector data from SL1."
        self.version = "2.0.0"
        self.add_step_parameter_from_object(region_param)

    def execute(self):
        region = self.get_parameter(region_param.name)
        super(PullAndProcessCollectors, self).execute()
        em7_response = self.get_current_saved_data()
        self.logger.debug(em7_response)

        if em7_response:
            snow_creates = []
            for collector in em7_response:
                sl_id = os.path.basename(collector['AA__key_val__'])
                snow_dict = {
                    "name": collector['name'],
                    "ip": collector['ip'],
                    "description": collector['descr'],
                    "id": sl_id,
                    "region": region,
                    "record_type": "collector"
                }
                snow_creates.append(snow_dict)

            if snow_creates:
                self.logger.flow(
                    u"Sending {} Collectors.".format(len(snow_creates)))
                self.logger.debug(u"snow_creates: {}".format(snow_creates))
                self.save_data_for_next_step(snow_creates)
            else:
                self.logger.flow(u"No Collectors to send.")
                self.save_data_for_next_step([])

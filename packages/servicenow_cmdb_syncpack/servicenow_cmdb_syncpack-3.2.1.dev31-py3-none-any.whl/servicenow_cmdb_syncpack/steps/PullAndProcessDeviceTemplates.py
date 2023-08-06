from os.path import basename

from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_base_syncpack.util.snow_parameters import region_param


class PullAndProcessDeviceTemplates(QueryREST):

    def __init__(self):
        super(PullAndProcessDeviceTemplates, self).__init__()
        self.friendly_name = "Process Device Templates"
        self.description = "Parse pulled Device Template data from SL1."
        self.version = "2.0.1"
        self.add_step_parameter_from_object(region_param)

    def execute(self):
        region = self.get_parameter(region_param.name)
        super(PullAndProcessDeviceTemplates, self).execute()
        em7_response = self.get_current_saved_data()
        self.logger.debug(em7_response)

        if em7_response:
            snow_creates = []
            for template in em7_response:
                snow_dict = {
                    "name": template['template_name'],
                    "id": basename(template['AA__key_val__']),
                    "region": region,
                    "record_type": "device_template"
                }
                snow_creates.append(snow_dict)
            if snow_creates:
                self.logger.flow(
                   u"Sending {} Device Templates.".format(len(snow_creates)))
                self.logger.debug(u"snow_creates: {}".format(snow_creates))

                self.save_data_for_next_step(snow_creates)
            else:
                self.logger.flow("No Device Templates to send.")
                self.save_data_for_next_step([])

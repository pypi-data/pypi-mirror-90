import os

from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascore import parameter_types


class PullAndProcessVirtualClasses(QueryREST):

    def __init__(self):
        super(PullAndProcessVirtualClasses, self).__init__()
        self.friendly_name = "Process Virtual Device Classes"
        self.description = "Parse pulled Virtual Device Class data from SL1."
        self.version = "2.0.0"
        self.new_step_parameter(
            name="region", default_value="ScienceLogicRegion",
            sample_value="ScienceLogicRegion",
            description="The region to input into CI information when posting "
                        "to snow",
            required=True, param_type=parameter_types.StringParameterShort())

    def execute(self):
        region = self.get_parameter("region")
        super(PullAndProcessVirtualClasses, self).execute()
        em7_response = self.get_current_saved_data()
        self.logger.debug(em7_response)

        if em7_response:
            snow_creates = []
            for vClass in em7_response:
                sl_id = os.path.basename(vClass['AA__key_val__'])
                snow_dict = {
                    "class": vClass['class'],
                    "description": vClass['description'],
                    "id": sl_id,
                    "region": region,
                    "record_type": "virtual_device_class",
                    "name": "{} | {}".format(
                        vClass['class'], vClass['description']
                    )
                }
                snow_creates.append(snow_dict)

            if snow_creates:
                self.logger.flow(
                    "Sending {} Virtual Device Classes.".format(
                        len(snow_creates)
                    ))
                self.logger.debug(u"snow_creates: {}".format(snow_creates))
                self.save_data_for_next_step(snow_creates)
            else:
                self.logger.flow("No Classes to send.")
                self.save_data_for_next_step([])

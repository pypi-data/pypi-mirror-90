from base_steps_syncpack.steps.QueryREST import QueryREST
from ipaascore import parameter_types
import os


class PostandParseSL1Org(QueryREST):

    def __init__(self):
        super(PostandParseSL1Org, self).__init__()
        self.friendly_name = "Post Org to SL1 and Process Response"
        self.description = "Processes response from Org post to send " \
                           "Org ID back to ServiceNow"
        self.version = "2.0.0"
        self.new_step_parameter(
            name="slregion",
            description="Unique Identifier for SL/IS instance.",
            required=True, default_value="ScienceLogicRegion",
            param_type=parameter_types.StringParameterShort()
        )

    def execute(self):
        region = self.get_parameter("slregion")
        super(PostandParseSL1Org, self).execute()
        em7_response = self.get_current_saved_data()
        self.logger.flow(em7_response)

        if em7_response:
            slid = os.path.basename(em7_response.get('location'))
            crm_id = em7_response.get('crm_id')
            snow_payload = {
                "records": [
                    {
                        "crm_id": crm_id,
                        "region": region,
                        "id": slid
                    }
                ]
            }
            self.logger.flow(u"SNOW Payload: {}".format(snow_payload))
            self.save_data_for_next_step(snow_payload)

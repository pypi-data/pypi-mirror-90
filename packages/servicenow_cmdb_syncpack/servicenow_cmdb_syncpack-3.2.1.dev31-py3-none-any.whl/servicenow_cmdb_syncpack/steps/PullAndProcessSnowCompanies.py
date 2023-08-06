import pickle

from base_steps_syncpack.steps.QueryREST import QueryREST
from servicenow_cmdb_syncpack.util.org_utils import ServiceNowCompany


class PullAndProcessSnowCompanies(QueryREST):
    def __init__(self):
        super(PullAndProcessSnowCompanies, self).__init__()
        self.friendly_name = "Pull and Process ServiceNow Companies"
        self.description = (
            "Pulls Companies from ServiceNow and converts them into ServiceNowCompany objects."
        )
        self.version = "1.0.0"

    def execute(self):
        super(PullAndProcessSnowCompanies, self).execute()
        result = self.get_current_saved_data()
        self.logger.flow(f"Pulled {len(result)} Companies from ServiceNow.")
        self.logger.info(f"Pulled Companies: {result}")
        processed_companies = dict()
        for company in result:
            snow_company = ServiceNowCompany(company)
            processed_companies[snow_company.snow_sys_id] = snow_company

        self.save_data_for_next_step(pickle.dumps(processed_companies))

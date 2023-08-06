from base_steps_syncpack.steps.QueryREST import QueryREST


class PullCompaniesFromServiceNow(QueryREST):
    def __init__(self):
        super(PullCompaniesFromServiceNow, self).__init__()
        self.friendly_name = "Pull Companies from ServiceNow"
        self.description = "Pulls Companies from ServiceNow and formats result."
        self.version = "1.0.0"

    def execute(self):
        super(PullCompaniesFromServiceNow, self).execute()
        results = self.get_current_saved_data()
        processed_result = dict()
        for result in results:
            if result.get("sys_id"):
                processed_result[result["sys_id"]] = result
            else:
                continue

        self.save_data_for_next_step(processed_result)

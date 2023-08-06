from base_steps_syncpack.steps.MySqlSelect import MySqlSelect


class FetchParentDevices(MySqlSelect):
    def __init__(self):
        super(FetchParentDevices, self).__init__()
        self.friendly_name = "Fetch Parent Devices from SL1"
        self.description = "Pulls DCM relations from the master_dev.component_dev_map table."
        self.version = "1.0.0"

    def execute(self):
        super(FetchParentDevices, self).execute()
        results = self.get_current_saved_data()
        processed_result = dict()
        for result in results:
            if result.get("id"):
                processed_result[result["id"]] = result
            else:
                continue

        self.save_data_for_next_step(processed_result)

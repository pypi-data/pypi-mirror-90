from base_steps_syncpack.steps.QueryGQL import QueryGQL


class GetDevicesFromSL1(QueryGQL):
    def __init__(self):
        super(GetDevicesFromSL1, self).__init__()
        self.friendly_name = "Pull SL1 Devices Using GQL query"
        self.description = "Pulls Devices from SL1 and formats result."
        self.version = "1.0.0"

    def execute(self):
        super(GetDevicesFromSL1, self).execute()
        device_class = self.get_current_saved_data()
        device_list = []
        for classes in device_class:
            device_list.append(
                f"{classes['node']['deviceClass']['class']} | {classes['node']['deviceClass']['description']}"
            )
        self.logger.debug(f"This is the device list is: {device_list}")
        self.save_data_for_next_step(device_list)

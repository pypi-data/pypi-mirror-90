from base_steps_syncpack.steps.QueryREST import QueryREST


class RaiseEvent(QueryREST):
    def __init__(self):
        super(RaiseEvent, self).__init__()
        self.friendly_name = "Raise an event in SL1"
        self.description = "Raises an event in SL1 if Class Mappings are missing"
        self.version = "1.0.0"

    def execute(self):
        payload = self.get_data_from_step_by_name("Process Device Classes")
        if payload["enabled"]:
            super(RaiseEvent, self).execute()
        else:
            self.logger.flow("No Missing Classes found, disabling step...")

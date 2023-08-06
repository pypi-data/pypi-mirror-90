from base_steps_syncpack.steps.MySqlSelect import MySqlSelect


class PullAndProcessHardwareModels(MySqlSelect):

    def __init__(self):
        super(PullAndProcessHardwareModels, self).__init__()
        self.friendly_name = "Pull And Process Hardware Models"
        self.description = "Parse pulled asset data from SL1 and ServiceNow"
        self.version = "2.0.0"

    def execute(self):
        super(PullAndProcessHardwareModels, self).execute()
        sl1_assets = self.get_current_saved_data()

        self.logger.debug(u"sl1_asset: {}".format(sl1_assets))

        models = []

        self.logger.info("Starting hardware search.")
        for asset in sl1_assets:
            if asset['model']:
                models.append(asset['model'])
            else:
                continue

        self.logger.flow(
            "Sending {} Hardware Models to ServiceNow for Matching.".format(
                len(models)
            )
        )
        self.logger.debug(u"Models: {}".format(models))
        self.save_data_for_next_step(
            {
                "models": models
            }
        )

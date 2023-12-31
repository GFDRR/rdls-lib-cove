from collections import defaultdict

from libcoverdls.base_task import AdditionalCheck


class StatisticHazardDatasets(AdditionalCheck):
    def __init__(self, lib_cove_rdls_config, schema_object):
        super().__init__(lib_cove_rdls_config, schema_object)
        self.stat = 0

    def check_hazard_dataset_first_pass(self, statement):
        self.stat += 1

    def get_statistics(self):
        return {
            "count_hazard_datasets": self.stat,
        }


class StatisticExposureDatasets(AdditionalCheck):
    def __init__(self, lib_cove_rdls_config, schema_object):
        super().__init__(lib_cove_rdls_config, schema_object)
        self.stat = 0

    def check_exposure_dataset_first_pass(self, statement):
        self.stat += 1

    def get_statistics(self):
        return {
            "count_exposure_datasets": self.stat,
        }


class StatisticVulnerabilityDatasets(AdditionalCheck):
    def __init__(self, lib_cove_rdls_config, schema_object):
        super().__init__(lib_cove_rdls_config, schema_object)
        self.stat = 0

    def check_vulnerability_dataset_first_pass(self, statement):
        self.stat += 1

    def get_statistics(self):
        return {
            "count_vulnerability_datasets": self.stat,
        }


class StatisticLossDatasets(AdditionalCheck):
    def __init__(self, lib_cove_rdls_config, schema_object):
        super().__init__(lib_cove_rdls_config, schema_object)
        self.stat = 0

    def check_loss_dataset_first_pass(self, statement):
        self.stat += 1

    def get_statistics(self):
        return {
            "count_loss_datasets": self.stat,
        }

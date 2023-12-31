class AdditionalCheck:
    """Any check or statistic that wants to be provided should extend this abstract class and overwrite methods.

    Methods to find out info about this class are static, so the class is only instantiated
    if data is really going to be run through it.
    This means in __init__ you can set up any storage you need, knowing that it will be used.
    """

    def __init__(self, lib_cove_rdls_config, schema_object):
        self._additional_check_results = []
        self._lib_cove_rdls_config = lib_cove_rdls_config
        self._schema_object = schema_object

    @staticmethod
    def get_additional_check_types_possible(
        lib_cove_rdls_config, schema_object
    ) -> list:
        """This should list all the additional check "type" keys that are possible might be emitted from this class,
        for the given config and schema."""
        return []

    @staticmethod
    def does_apply_to_schema(lib_cove_rdls_config, schema_object) -> bool:
        return True

    def check_dataset_first_pass(self, statement):
        pass

    def check_hazard_dataset_first_pass(self, statement):
        pass

    def check_exposure_dataset_first_pass(self, statement):
        pass

    def check_vulnerability_dataset_first_pass(self, statement):
        pass

    def check_loss_dataset_first_pass(self, statement):
        pass

    def check_hazard_dataset_second_pass(self, statement):
        pass

    def check_exposure_dataset_second_pass(self, statement):
        pass

    def check_vulnerability_dataset_second_pass(self, statement):
        pass

    def check_loss_dataset_second_pass(self, statement):
        pass

    def final_checks(self):
        pass

    def get_additional_check_results(self):
        return self._additional_check_results

    def get_statistics(self):
        return {}

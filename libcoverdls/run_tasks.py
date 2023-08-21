import libcoverdls.data_reader
import libcoverdls.tasks.checks
import libcoverdls.tasks.statistics

TASK_CLASSES = [
#    libcoverdls.tasks.checks.LegacyChecks,
#    libcoverdls.tasks.checks.LegacyChecksNeedingHistory,
#    libcoverdls.tasks.checks.CheckHasPublicListing,
#    libcoverdls.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
#    libcoverdls.tasks.checks.CheckEntitySecurityListingsMICSCodes,
#    libcoverdls.tasks.statistics.LegacyStatistics,
#    libcoverdls.tasks.statistics.StatisticsCurrentOwnershipOrControlStatementsAndReplacesStatementsMissing,
#    libcoverdls.tasks.statistics.StatisticAddress,
#    libcoverdls.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
#    libcoverdls.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
#    libcoverdls.tasks.peps.PEPForSchema02Only,
#    libcoverdls.tasks.peps.PEPForSchema03AndAbove,
    libcoverdls.tasks.statistics.StatisticHazardDatasets,
    libcoverdls.tasks.statistics.StatisticExposureDatasets,
    libcoverdls.tasks.statistics.StatisticVulnerabilityDatasets,
    libcoverdls.tasks.statistics.StatisticLossDatasets,
]

TASK_CLASSES_IN_SAMPLE_MODE = [
#    libcoverdls.tasks.checks.LegacyChecks,
#    libcoverdls.tasks.checks.CheckHasPublicListing,
#    libcoverdls.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
#    libcoverdls.tasks.checks.CheckEntitySecurityListingsMICSCodes,
#    libcoverdls.tasks.statistics.LegacyStatistics,
#    libcoverdls.tasks.statistics.StatisticAddress,
#    libcoverdls.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
#    libcoverdls.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
#    libcoverdls.tasks.peps.PEPForSchema02Only,
#    libcoverdls.tasks.peps.PEPForSchema03AndAbove,
]


def process_additional_checks(
    data_reader: libcoverdls.data_reader.DataReader,
    lib_cove_rdls_config,
    schema_object,
    task_classes=TASK_CLASSES,
):
    additional_check_instances = [
        x(lib_cove_rdls_config, schema_object)
        for x in task_classes
        if x.does_apply_to_schema(lib_cove_rdls_config, schema_object)
    ]
    all_data = data_reader.get_all_data()

    # First pass
    for dataset in all_data:
        risk_data_type = dataset.get("risk_data_type")
        for additional_check_instance in additional_check_instances:
            additional_check_instance.check_dataset_first_pass(dataset)
        if risk_data_type == "hazard":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_hazard_dataset_first_pass(dataset)
        elif risk_data_type == "exposure":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_exposure_dataset_first_pass(dataest)
        elif risk_data_type == "vulnerability":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_vulnerability_dataset_first_pass(dataset)
        elif risk_data_type == "loss":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_loss_dataset_first_pass(dataset)

    # Second Pass
    for dataset in all_data:
        risk_data_type = dataset.get("risk_data_type")
        if risk_data_type == "hazard":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_hazard_dataset_second_pass(dataset)
        elif risk_data_type == "exposure":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_exposure_dataset_second_pass(dataset)
        elif risk_data_type == "vulnerability":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_vulnerability_dataset_second_pass(dataset)
        elif risk_data_type == "loss":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_loss_dataset_second_pass(dataset)

    # Final checks
    for additional_check_instance in additional_check_instances:
        additional_check_instance.final_checks()

    # Get results
    additional_checks = []
    statistics = {}
    if schema_object.schema_error:
        additional_checks.append(schema_object.schema_error)
    for additional_check_instance in additional_check_instances:
        additional_checks.extend(
            additional_check_instance.get_additional_check_results()
        )
        statistics.update(additional_check_instance.get_statistics())
    return {"additional_checks": additional_checks, "statistics": statistics}

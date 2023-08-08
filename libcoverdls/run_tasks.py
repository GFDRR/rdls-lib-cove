import libcoverdls.data_reader
import libcoverdls.tasks.checks
import libcoverdls.tasks.peps
import libcoverdls.tasks.statistics

TASK_CLASSES = [
    libcoverdls.tasks.checks.LegacyChecks,
    libcoverdls.tasks.checks.LegacyChecksNeedingHistory,
    libcoverdls.tasks.checks.CheckHasPublicListing,
    libcoverdls.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
    libcoverdls.tasks.checks.CheckEntitySecurityListingsMICSCodes,
    libcoverdls.tasks.statistics.LegacyStatistics,
    libcoverdls.tasks.statistics.StatisticsCurrentOwnershipOrControlStatementsAndReplacesStatementsMissing,
    libcoverdls.tasks.statistics.StatisticAddress,
    libcoverdls.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    libcoverdls.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    libcoverdls.tasks.peps.PEPForSchema02Only,
    libcoverdls.tasks.peps.PEPForSchema03AndAbove,
]

TASK_CLASSES_IN_SAMPLE_MODE = [
    libcoverdls.tasks.checks.LegacyChecks,
    libcoverdls.tasks.checks.CheckHasPublicListing,
    libcoverdls.tasks.checks.CheckEntityTypeAndEntitySubtypeAlign,
    libcoverdls.tasks.checks.CheckEntitySecurityListingsMICSCodes,
    libcoverdls.tasks.statistics.LegacyStatistics,
    libcoverdls.tasks.statistics.StatisticAddress,
    libcoverdls.tasks.statistics.StatisticOwnershipOrControlInterestDirectOrIndirect,
    libcoverdls.tasks.statistics.StatisticOwnershipOrControlWithAtLeastOneInterestBeneficial,
    libcoverdls.tasks.peps.PEPForSchema02Only,
    libcoverdls.tasks.peps.PEPForSchema03AndAbove,
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
    for statement in all_data:
        statement_type = statement.get("statementType")
        for additional_check_instance in additional_check_instances:
            additional_check_instance.check_statement_first_pass(statement)
        if statement_type == "entityStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_entity_statement_first_pass(statement)
        elif statement_type == "personStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_person_statement_first_pass(statement)
        elif statement_type == "ownershipOrControlStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_ownership_or_control_statement_first_pass(
                    statement
                )

    # Second Pass
    for statement in all_data:
        statement_type = statement.get("statementType")
        if statement_type == "entityStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_entity_statement_second_pass(statement)
        elif statement_type == "personStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_person_statement_second_pass(statement)
        elif statement_type == "ownershipOrControlStatement":
            for additional_check_instance in additional_check_instances:
                additional_check_instance.check_ownership_or_control_statement_second_pass(
                    statement
                )

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

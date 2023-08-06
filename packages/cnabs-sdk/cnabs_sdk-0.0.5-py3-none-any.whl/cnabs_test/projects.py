import cnabssdk
import cnabssdk.projects
import cnabs_test.tools


def run_test(token):
    cnabssdk.init(token)
    passed = cnabssdk.projects.get_projects("", "2020-11-1", "2020-11-30", '通过')
    print("passed: " + str(len(passed)))
    cnabs_test.tools.print_tables(passed)

    exchanges = cnabssdk.projects.get_statistic_by_exchanges('2020-11-1', '2020-11-30')
    cnabs_test.tools.print_tables(exchanges)

    firstObj = passed[0]
    cnabs_test.tools.print_object(firstObj)

    timelines = cnabssdk.projects.get_project_timelines(firstObj.id)
    cnabs_test.tools.print_tables(timelines)

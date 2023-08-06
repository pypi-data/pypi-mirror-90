import cnabs_test.tools
import cnabssdk
import cnabssdk.organizations

def run_test(token):
    cnabssdk.init(token)
    industries = cnabssdk.organizations.get_industries()
    cnabs_test.tools.print_tables(industries)

    orgList = cnabssdk.organizations.get_organizations('中信证券股份有限公司')
    print('org length: ' + str(len(orgList)))
    cnabs_test.tools.print_tables(orgList)

    orgName = orgList[0].name

    print('get org detail: ' + orgName)
    orgInfo = cnabssdk.organizations.get_organization(orgName)
    cnabs_test.tools.print_object(orgInfo)

    print('get ratings: ')
    ratings = cnabssdk.organizations.get_organization_ratings(orgName)
    cnabs_test.tools.print_tables(ratings)

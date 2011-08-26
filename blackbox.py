#!/usr/bin/python

import sys
# check python version
# In python 2.7 or upper, we need to use the argparse instead of optparse
if sys.version_info[:2] < (2, 7):
    from optparse import OptionParser
else:
    from argparse import ArgumentParser
# import all the API testing file
import src.authToken as authToken
import src.userRead as userRead
import src.userInfoRead as userInfoRead
import src.xmlSchema as xmlSchema
import src.campCret as campCret
import src.campDel as campDel
import src.campUp as campUp

# write to a file
# report is the succ/err report list generated by each API
def write_report_to_file(report, file_path, mode):
    # mode = 'w': write to a file
    # mode = 'a': append to a file
    try:
        f = open(file_path, mode)
        for x in report:
            f.write(x + '\n')
        f.close
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)

# write to standard output
def write_report_to_std(report):
    for x in report:
        print x

def main():
    usage_msg = "%prog [OPTION] ... arg1, arg2 ...\n\n" +\
                "Perform black box testing on AndWellness or Mobilizing server."
    version_msg = "%prog 2.6"
    
    # check python version
    # In python 2.7 or upper, we need to use the argparse instead of optparse
    if sys.version_info[:2] < (2, 7):
        parser = OptionParser(version=version_msg, usage=usage_msg)
    else:
        parser = ArgumentParser(version=version_msg, usage=usage_msg)
    
    # TODO: add more options if needed
    parser.add_option("--api", action="store", dest="API_NAME", default="all",
                      help="""Choose a specific API to test. By default, all those APIs will be tested.
Argument must from {auth_token, user_read, user_info_read, xml, camp_cret, camp_del, camp_up, all}""")
    parser.add_option("-f", "--file",
                      action="store", dest="FILE", default="report.log",
                      help = "Print the output to a file with filename FILE. By default, print to ./report.log")
    parser.add_option("-p", "--print",
                      action="store", dest="PRINT_MODE", default="all",
                      help = """Choose to print to screen or save the result to a log file.
Argument must from {std, file, all}""")
    parser.add_option("-r", "--result",
                      action="store", dest="RESULT", default="all",
                      help = """Choose to print or save success message or print or save error message.
Argument must from {succ, err, all}""")
    parser.add_option("-s", "--server",
                      action="store", dest="SERVER", default="and",
                      help = """Choose to run on AndWellness server or Mobilizing server. Default is AndWellness Server.
Argument must from {and, mob}""")   
    options, args = parser.parse_args(sys.argv[1:])
    
    api_req = ['auth_token', 'user_read', 'user_info_read', 'xml', 'camp_cret', 'camp_del', 'camp_up', 'all']
    print_req = ['std', 'file', 'all']
    result_req = ['succ', 'err', 'all']
    server_req = ['mob', 'and']
    
    # check for input arguments
    if api_req.count(options.API_NAME.lower()) == 0:
        parser.error("Invalid API_NAME: {0}".format(options.API_NAME))
    if print_req.count(options.PRINT_MODE.lower()) == 0:
        parser.error("Invalid PRINT_MODE: {0}".format(options.PRINT_MODE))
    if result_req.count(options.RESULT.lower()) == 0:
        parser.error("Invalid RESULT: {0}".format(options.RESULT))
    if server_req.count(options.SERVER.lower()) == 0:
        parser.error("Invalid SERVER: {0}".format(options.SERVER))
    
    # Use two list to hold all the successful report or error report
    succ_report = []    # notice that it is a list of list
    err_report = []     # notice that it is a list of list
    total_case = 0
    unexpect_case = 0
    invalid_case_id_list = []   # notice that it is a list of list
    # bind API to a list
    blackbox_test_api = []
    
    if options.API_NAME.lower() == 'auth_token':
        blackbox_test_api = [authToken.authToken_test(options.SERVER)]
    elif options.API_NAME.lower() == 'user_read':
        blackbox_test_api = [userRead.userRead_test(options.SERVER)]
    elif options.API_NAME.lower() == 'user_info_read':
        blackbox_test_api = [userInfoRead.userInfoRead_test(options.SERVER)]
    elif options.API_NAME.lower() == 'xml':
        blackbox_test_api = [xmlSchema.xmlSchema_test(options.SERVER)]
    elif options.API_NAME.lower() == 'camp_cret':
        blackbox_test_api = [campCret.campCret_test(options.SERVER)]
    elif options.API_NAME.lower() == 'camp_del':
        blackbox_test_api = [campDel.campDel_test(options.SERVER)]
    elif options.API_NAME.lower() == 'camp_up':
        blackbox_test_api = [campUp.campUp_test(options.SERVER)]
    elif options.API_NAME.lower() == 'all':
        blackbox_test_api = [authToken.authToken_test(options.SERVER),\
                             userRead.userRead_test(options.SERVER),\
                             userInfoRead.userInfoRead_test(options.SERVER),\
                             xmlSchema.xmlSchema_test(options.SERVER),\
                             campCret.campCret_test(options.SERVER),\
                             campDel.campDel_test(options.SERVER),\
                             campUp.campUp_test(options.SERVER)]
    else:
        print >> sys.stderr, 'Error: Invalid input for API_NAME'
        sys.exit(1)
    
    # Run all the APIs requested
    for api in blackbox_test_api:
        api.blackbox_test()
        total_case = total_case + api.total_case
        unexpect_case = unexpect_case + api.unexpect_case
        succ_report.append(api.succ_report)
        err_report.append(api.err_report)
        invalid_case_id_list.append(api.invalid_case_id_list)
        
    sum_report = ['Summary Section:',\
                  'Total number of cases: {0}'.format(total_case),\
                  'Total successful cases: {0}'.format(total_case-unexpect_case),\
                  'Total unexpected cases: {0}'.format(unexpect_case),\
                  'Here is a list of unexpected case ID: {0}'.format(invalid_case_id_list)]
    
    # Output request file to request place
    if options.PRINT_MODE.lower() == 'std':
        if options.RESULT.lower() == 'succ':
            for x in succ_report:
                write_report_to_std(x)
        elif options.RESULT.lower() == 'err':
            for x in err_report:
                write_report_to_std(x)
        else:
            # print all successful and error report
            for x in succ_report:
                write_report_to_std(x)
            for x in err_report:
                write_report_to_std(x)
    elif options.PRINT_MODE.lower() == 'file':
        if options.RESULT.lower() == 'succ':
            for x in succ_report:
                write_report_to_file(x, options.FILE, 'a')
        elif options.RESULT.lower() == 'err':
            for x in err_report:
                write_report_to_file(x, options.FILE, 'a')
        else:
            # print all successful and error report
            for x in succ_report:
                write_report_to_file(x, options.FILE, 'a')
            for x in err_report:
                write_report_to_file(x, options.FILE, 'a')
    else:
        # print to both standard output and file
        if options.RESULT.lower() == 'succ':
            for x in succ_report:
                write_report_to_std(x)
            for x in succ_report:
                write_report_to_file(x, options.FILE, 'a')
        elif options.RESULT.lower() == 'err':
            for x in err_report:
                write_report_to_std(x)
            for x in err_report:
                write_report_to_file(x, options.FILE, 'a')
        else:
            # print all successful and error report
            for x in succ_report:
                write_report_to_std(x)
            for x in err_report:
                write_report_to_std(x)
            for x in succ_report:
                write_report_to_file(x, options.FILE, 'a')
            for x in err_report:
                write_report_to_file(x, options.FILE, 'a')
    
    # Write summary to request place
    if options.PRINT_MODE.lower() == 'std':
        write_report_to_std(sum_report)
    elif options.PRINT_MODE.lower() == 'file':
        write_report_to_file(sum_report, options.FILE, 'a')
    else:
        write_report_to_std(sum_report)
        write_report_to_file(sum_report, options.FILE, 'a')
        
if __name__ == "__main__":
    main()
    
    

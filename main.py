import sys
import traceback

import graphs
import ip_parser
order = 16

def printHelp():
  print("""
    Usage:
    
    ./main.py <command> [options]
    
    Commands:
    parse <input file>
    graph_density <input file>
    graph_ports <input file>
    graph_nonstandard_ports <input file>
    generate_random_ips <input file> <count>
  """)

if __name__ == '__main__':
    try:
        argv = sys.argv
        match argv[1]:
            case 'parse':
                for ip in ip_parser.process_ips(sys.argv[2], verbose=False):
                    print(ip)
            case 'graph_density':
                graphs.graph_density(ip_parser.process_ips(sys.argv[2]))
            case 'graph_ports':
                graphs.graph_ports(ip_parser.process_ips(sys.argv[2]))
            case 'graph_nonstandard_ports':
                graphs.graph_nonstandard_ports(ip_parser.process_ips(sys.argv[2]))
            case 'generate_random_ips':
                graphs.generate_random_ips(ip_parser.process_ips(sys.argv[2]), int(sys.argv[3]))
            case _:
                printHelp()
    except Exception as e:
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
        print(str(e))
        printHelp()
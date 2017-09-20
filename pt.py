import os, sys, time
from optparse import OptionParser

MONITOR_INTERVAL_SEC = 6 #freshing intervals(seconds)

#f: file stream
#N(-n): number of lines to print at time
#monitor_on(-F) : whether to monitor input realtime
def tail(f,N,monitor_on):
    f.seek(0,os.SEEK_END)
    current_line_count =0
    finished = False

    while not finished:
        current_position = f.tell()
        line_of_input = f.readline()
        #print "1.line#:", current_line_count, ",seek current_pos:", current_position,

        if not line_of_input:#no data
            f.seek(current_position)
            finished = True
        else: #has data
            current_line_count += 1
            print line_of_input ,
            if current_line_count == N:
                current_line_count = 0
                finished = True

        if monitor_on and finished:#only for the option (-F)
            finished = False #to start over
            time.sleep(MONITOR_INTERVAL_SEC)

def main():

    parser = OptionParser(usage="usage: %prog [options] filename",
                               version="%prog 1.0")
    parser.add_option("-n", type="int", dest="num_of_lines", default=10, help="number of lines to print")
    parser.add_option("-F", dest="monitor_on", action="store_true",
            default=False, help="to monitor input realtime refreshing every # seconds")  #MONITOR_INTERVAL_SEC
    

    (options, args) = parser.parse_args()
    
    #input check
    if len(args) < 1:
        print "Please include filename after the options ex) -n 10 -F access.log"
        quit()
    
    if options.num_of_lines is None:#if not a number
        print "Please enter a number for -n options ex) -n 10"
        quit()

    #debug purpose for the input value
    print '(-n)Number of Lines to print=' , options.num_of_lines
    print '(-F)monitor_on=' , options.monitor_on
    print 'filename=' , args[0]
    
    filename = args[0]
    num_of_lines = options.num_of_lines
    monitor_on =  options.monitor_on

    try:
        with open(filename) as f:
            tail(f,num_of_lines,monitor_on)
    except Exception as e:
        print "[Please check error]", str(e)


if __name__ == '__main__':

    main()

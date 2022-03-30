import sys
def logging(log_message):
    log_name = sys.path[0]+'\\'+str(datetime.date.today())+'.txt'
    if os.path.exists(log_name):
        log = open(log_name,"a")
    else:
        log = open(log_name, "w")
    log.write(str(datetime.datetime.now()) +' '+log_message + '\n')
    log.close()
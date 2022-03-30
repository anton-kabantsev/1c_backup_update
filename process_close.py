import log, subprocess
def spaces_deletion(str):
    string = ''
    ind = 0
    for i in str.split():
        if ind > 0:
            string = string +' '+i.strip()
        else:
            string = string + i.strip()
        ind = ind +1
    return string

def tasklist_parse(str):
    output = str.split('   ')
    pars_res = {'image_name':1,'pid':1,'session_name':1,'session_number':1,'memory':1}
    for i in output:
        session_str = spaces_deletion(i)
        if len(session_str)>0:
            if pars_res['image_name']==1:
                pars_res['image_name'] = session_str
            elif pars_res['pid'] ==1:
                pars_res['pid'] = session_str.split(' ')[0]
                pars_res['session_name'] = session_str.split(' ')[1]
            elif pars_res['session_number'] ==1 :
                pars_res['session_number'] = session_str
            elif pars_res['memory'] == 1:
                pars_res['memory'] = session_str
    return pars_res

def console(command,split=True):
    try:
        result = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        if split:
            return result.decode('cp866').split("\n")
        else:
            return result.decode('cp866')
    except subprocess.CalledProcessError as exc:
        log.logging("Status : FAIL"+exc.output.decode('cp866'))
    return ('error')

def get_process(proc_name=''):
    if len(proc_name)==0:
        command = ["tasklist"]
        ind = 3
    else:
        command = ["tasklist","|findstr",proc_name]
        ind = 0
    output = console(command)
    if output=='error':
        pid_list = []
        return pid_list
    pid_list = []
    while ind != len(output):
        if len(spaces_deletion(output[ind]))>0:
            pars_res = (tasklist_parse(output[ind]))
            print(pars_res)
            pid_list.append(pars_res['pid'])
        ind = ind + 1
    return pid_list

def kill_proc(proc_name):
    pid_list = get_process(proc_name)
    if len(pid_list)==0:
        log.logging('1с не запущена')
        return 0
    for pid in pid_list:
        command = ['taskkill','/f','/pid',pid]
        console(command)
        #print(output)
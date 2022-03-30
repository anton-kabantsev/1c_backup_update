import random, subprocess, sys, time, datetime, os.path, zipfile

def logging(log_message):
    log_name = sys.path[1]+'\\'+str(datetime.date.today())+'.txt'
    if os.path.exists(log_name):
        log = open(log_name,"a")
    else:
        log = open(log_name, "w")
    log.write(str(datetime.datetime.now()) +' '+log_message + '\n')
    log.close()

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
        logging("Status : FAIL"+exc.output.decode('cp866'))
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
        logging('1с не запущена')
        return 0
    for pid in pid_list:
        command = ['taskkill','/f','/pid',pid]
        console(command)
        #print(output)

def default_backup_ini_creation(backup_ini_path):
    backup_ini = open(backup_ini_path, "w")
    backup_ini.write('**Файл настроек скрипта бэкапа' + '\n')
    backup_ini.write('**образец указания пути к 1с базе для бэкапа: BackupPath=C:\1c_bases\infobase' + '\n')
    backup_ini.write('**образец указания пути к каталогу для хранения бэкапа: BackupDSTPath=C:\backup' + '\n')
    backup_ini.close()

def read_settings():
    backup_ini_path = sys.path[0] + '\\' + 'backup.ini'
    if os.path.exists(backup_ini_path):
        backup_ini = open(backup_ini_path, "r")
        backup_list=[]
        backup_dst=''
        for line in backup_ini:
            if line.find('*')==-1:
                if line.find('BackupPath=')==0:
                    bak_path = line.replace('BackupPath=','').strip()
                    if os.path.exists(bak_path):
                        backup_list.append(bak_path)
                elif line.find('BackupDSTPath=')==0:
                    bak_path = line.replace('BackupDSTPath=', '').strip()
                    if os.path.exists(bak_path) :
                        backup_dst= bak_path
    else:
        default_backup_ini_creation(backup_ini_path)
        logging('backup.ini не существует в '+sys.path[0])
        logging('backup.ini создан ' + sys.path[0])
        backup_settings['result']=False
    backup_settings = {}
    backup_settings['backup_list']=backup_list
    backup_settings['backup_dst']=backup_dst
    backup_settings['result']=True
    return backup_settings

def get_name(bakpath):
    # получим имя бэкапа - имя папки + дата
    # имя папки:
    lst = bakpath.split('\\')
    return (lst[len(lst)-1]+'_'+str(datetime.date.today())+'.zip')

def create_backup(backup_settings):
    for bakpath in backup_settings['backup_list']:
        with zipfile.ZipFile(backup_settings['backup_dst']+'\\'+get_name(bakpath),'w') as backup:
            backup.write(bakpath+'\\1cv8.1cd')
            logging('Бэкап '+get_name(bakpath)+' создан')

def main():
    # Прочитать файл настроек. Назначение - хранение путей к базам для бэкапа
    logging('Начинаем бэкап 1с баз')
    backup_settings = read_settings()
    if backup_settings['result']==False:
        exit()
    logging('Настройки получены...')
    # Завершить процессы 1с
    logging('Завершаем процессы 1с')
    kill_proc('1c')
    logging('Создаем бэкапы')
    create_backup(backup_settings)
    logging('Процесс завершен')
main()
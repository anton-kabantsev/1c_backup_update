import sys, datetime, os.path, zipfile, log, process_close

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
        log.logging('backup.ini не существует в '+sys.path[0])
        log.logging('backup.ini создан ' + sys.path[0])
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
    return (lst[len(lst)-1]+'_'+datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'.zip')

def create_backup(backup_settings):
    for bakpath in backup_settings['backup_list']:
        with zipfile.ZipFile(backup_settings['backup_dst']+'\\'+get_name(bakpath),'w') as backup:
            backup.write(bakpath+'\\1cv8.1cd')
            log.logging('Бэкап '+get_name(bakpath)+' создан')

def remove_old_files(Number_to_keep,bak_name,backup_dst):
    bak_lst=[]
    for files in os.walk(backup_dst, topdown=True,onerror=None,followlinks=True):
        for name in files[2]:
            if name.find(bak_name)!=-1:
                bak_lst.append(backup_dst+'\\'+name)
                print(backup_dst+'\\'+name)
        break
    if len(bak_lst)==0:
        return 1
    elif len(bak_lst)<=Number_to_keep: # нечего удалять
        return 0
    while Number_to_keep<len(bak_lst):
        bak_to_del =''
        bak_date =''
        first_iter = True
        for bak in bak_lst:
            if first_iter:
                bak_date = os.path.getctime(bak)
                bak_to_del = bak
                first_iter = False
                continue
            if bak_date > os.path.getctime(bak):
                bak_date = os.path.getctime(bak)
                bak_to_del = bak
        bak_lst.remove(bak_to_del)
        os.remove(bak_to_del)

def clean_backup_dst(backup_settings,Number_to_keep):
    for bakpath in backup_settings['backup_list']:
        bak_name = bakpath.split('\\')[len(bakpath.split('\\'))-1]
        remove_old_files(Number_to_keep, bak_name, backup_settings['backup_dst'])


def main():
    # Прочитать файл настроек. Назначение - хранение путей к базам для бэкапа
    log.logging('Начинаем бэкап 1с баз')
    backup_settings = read_settings()
    if backup_settings['result']==False:
        exit()
    log.logging('Настройки получены...')
    # Завершить процессы 1с
    log.logging('Завершаем процессы 1с')
    process_close.kill_proc('1c')
    log.logging('Создаем бэкапы')
    create_backup(backup_settings)
    log.logging('Бэкап завершен')
    clean_backup_dst(backup_settings,8)
    log.logging('Очистка хранилища завершена')
    log.logging('Процесс завершен')
main()
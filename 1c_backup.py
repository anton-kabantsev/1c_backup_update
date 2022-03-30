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
    return (lst[len(lst)-1]+'_'+str(datetime.date.today())+'.zip')

def create_backup(backup_settings):
    for bakpath in backup_settings['backup_list']:
        with zipfile.ZipFile(backup_settings['backup_dst']+'\\'+get_name(bakpath),'w') as backup:
            backup.write(bakpath+'\\1cv8.1cd')
            log.logging('Бэкап '+get_name(bakpath)+' создан')

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
    log.logging('Процесс завершен')
main()
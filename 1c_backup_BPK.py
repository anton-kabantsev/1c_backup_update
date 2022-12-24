import sys, datetime, os.path, zipfile
from backup import log
from backup import process_close

def create_bak_list(sys_path,backup_folder,backup_dst):
    backfile_path = sys_path + '\\' + 'backup.ini'
    backfile_ini = open(backfile_path, "w")
    backfile_ini.write('** 1C bases backup list'+ '\n')
    backfile_ini.write('** File was created automatically.Do not edit!'+ '\n')

    bd_name = '1Cv8.1CD'
    bak_lst = []
    for files in os.walk(backup_folder, topdown=True, onerror=None, followlinks=True):
        for name in files[2]:
            if files[0].find('1Cv8FTxt')!=-1:
                break
            if name==bd_name:
                backfile_ini.write('BackupPath='+files[0] + '\\' + name+ '\n')
                print('BackupPath='+files[0] + '\\' + name)
    backfile_ini.write('BackupDSTPath='+backup_dst+ '\n')
    backfile_ini.close()

def read_settings(sys_path):
    backup_ini_path = sys_path + '\\' + 'backup.ini'
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
    backup_settings = {}
    backup_settings['backup_list']=backup_list
    backup_settings['backup_dst']=backup_dst
    backup_settings['result']=True
    return backup_settings

def get_name(bakpath):
    # получим имя бэкапа - имя папки + дата
    # имя папки:
    lst = bakpath.split('\\')
    name = ''
    first_pos = True
    for pos in lst:
        if first_pos:
            name = name+pos
            first_pos = False
        else:
            name = name+'_'+pos
    name = name.replace(':','')
    name = name.replace('.','_')
    return (name+'_'+datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'.zip')

def create_backup(backup_settings):
    for bakpath in backup_settings['backup_list']:
        with zipfile.ZipFile(backup_settings['backup_dst']+'\\'+get_name(bakpath),'w') as backup:
            backup.write(bakpath)
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
    # Настройки
    sys_path = 'D:\\temp\\24_12_2022'  # папка хранения ini файлов скрипта
    backup_folder = 'D:\\1c\\base'  # какую папку анализировать на базы и бэкапить
    backup_dst = 'D:\\1c_backup'  # куда кидать бэкапы
    number_to_keep = 3 # Enter number of backup to keep for every base
    # Прочитать файл настроек. Назначение - хранение путей к базам для бэкапа
    log.logging('Начинаем бэкап 1с баз')
    # Создание файла настроек
    create_bak_list(sys_path,backup_folder, backup_dst)
    backup_settings = read_settings(sys_path)
    if backup_settings['result']==False:
        exit()
    log.logging('Настройки получены...')
    # Завершить процессы 1с
    log.logging('Завершаем процессы 1с')
    process_close.kill_proc('1c')
    log.logging('Создаем бэкапы')
    create_backup(backup_settings)
    log.logging('Бэкап завершен')
    clean_backup_dst(backup_settings,number_to_keep)
    log.logging('Очистка хранилища завершена')
    log.logging('Процесс завершен')
main()
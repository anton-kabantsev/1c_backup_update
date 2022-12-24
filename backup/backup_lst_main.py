# backup list maintanance functions - create list, check list, modify list
import os, sys, datetime

def create_bak_list(backup_folder,backup_dst):
    backfile_path = sys.path[0] + '\\' + 'backup_bd_list.txt'
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
    backfile_ini.write('BackupDSTPath=='+backup_dst+ '\n')
    backfile_ini.close()

def main():
    create_bak_list('D:\\1c\\base','D:\\1c_backup')

main()
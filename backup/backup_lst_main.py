# backup list maintanance functions - create list, check list, modify list
import os


def create_bak_list(backup_dst):
    bd_name = '1Cv8.1CD'
    bak_lst = []
    for files in os.walk(backup_dst, topdown=True, onerror=None, followlinks=True):
        for name in files[2]:
            if name==bd_name:
                bak_lst.append(backup_dst + '\\' + name)
                print(files[0] + '\\' + name)


def main():
    create_bak_list('D:\\1c\\base')

main()
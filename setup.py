#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2021/01/08 17:05:09
@Author  :   bigfirmament
@Contact :   bigfirmament@163.com
@Desc    :   setup file
'''

# here put the import lib
from job import GetAliEcsDevopsServiceBackupData


if __name__ == "__main__":
    backupJob = GetAliEcsDevopsServiceBackupData.BackupData()
    backupJob.excute_backup_jod()
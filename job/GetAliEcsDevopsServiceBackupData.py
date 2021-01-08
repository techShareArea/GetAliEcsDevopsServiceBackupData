#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   GetAliEcsDevopsServiceBackupData.py
@Time    :   2021/01/08 17:06:17
@Author  :   bigfirmament
@Contact :   bigfirmament@163.com
@Desc    :   None
'''

# here put the import lib
import time
import subprocess
from docs import config


class BackupData():
    def __init__(self, current_date=time.strftime("%Y%m%d")):
        self.current_date = current_date
        self.ali_ecs_ip = config.ali_ecs_ip
        self.ali_ecs_user = config.ali_ecs_user
        self.remote_connect_port = config.remote_connect_port
        self.ali_ecs_user_ops_passwd = config.ali_ecs_user_ops_passwd
        self.ali_ecs_pms_clean_dir = config.ali_ecs_pms_clean_dir
        self.ali_ecs_jenkins_clean_dir = config.ali_ecs_jenkins_clean_dir
        self.ali_ecs_gitlab_clean_dir = config.ali_ecs_gitlab_clean_dir
        self.ali_ecs_pms_backup_dir = config.ali_ecs_pms_backup_dir
        self.internal_service_pms_backup_dir = config.internal_service_pms_backup_dir
        self.internal_service_gitlab_backup_dir = config.internal_service_gitlab_backup_dir
        self.internal_service_jenkins_backup_dir = config.internal_service_jenkins_backup_dir
        self.ali_ecs_jenkins_source_backup_file_name = config.ali_ecs_jenkins_source_backup_file_name

    def excute_command(self, command):
        subp = subprocess.Popen(command,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if subp.poll() != 0:
            return subp.stdout.read().decode("gbk").encode("utf-8")
        else:
            return "failure"

    def get_ali_ecs_pms_backup_data(self):
        current_date = time.strftime("%Y%m%d")

        if "01" == current_date[-2::]:
            remote_backup_pms_dir = self.ali_ecs_pms_backup_dir
        else:
            remote_backup_pms_dir = self.ali_ecs_pms_clean_dir
        excute_scp_ali_ecs_pms_to_internal = "sshpass -p {0} scp -oPort={1} -o stricthostkeychecking=no -r {2}@{3}:{4}{5} {6}{5}".format(
            self.ali_ecs_user_ops_passwd, self.remote_connect_port,
            self.ali_ecs_user, self.ali_ecs_ip, remote_backup_pms_dir,
            current_date, self.internal_service_pms_backup_dir)
        return excute_scp_ali_ecs_pms_to_internal

    def get_ali_ecs_others_backup_data(self):
        if time.strftime("%a", time.localtime()) == "Sun":
            excute_scp_ali_ecs_gitlab_to_internal = "sshpass -p {0} scp -oPort={1} -o stricthostkeychecking=no -r {2}@{3}:{4}*.tar {5}".format(
                self.ali_ecs_user_ops_passwd, self.remote_connect_port,
                self.ali_ecs_user, self.ali_ecs_ip,
                self.ali_ecs_gitlab_clean_dir,
                self.internal_service_gitlab_backup_dir)
            return excute_scp_ali_ecs_gitlab_to_internal
        elif time.strftime("%a", time.localtime()) == "Sat":
            excute_scp_ali_ecs_jenkins_to_internal = "sshpass -p {0} scp -oPort={1} -o stricthostkeychecking=no -r {2}@{3}:{4}{5}.bak{6}.tar {7}".format(
                self.ali_ecs_user_ops_passwd, self.remote_connect_port,
                self.ali_ecs_user, self.ali_ecs_ip,
                self.ali_ecs_jenkins_clean_dir,
                self.ali_ecs_jenkins_source_backup_file_name,
                self.current_date, self.internal_service_jenkins_backup_dir)
            return excute_scp_ali_ecs_jenkins_to_internal

    def excute_backup_jod(self):
        get_excute_backup_pms_command = BackupData().get_ali_ecs_pms_backup_data()
        BackupData().excute_command(get_excute_backup_pms_command)
        get_excute_backup_others_command = BackupData().get_ali_ecs_others_backup_data()
        BackupData().excute_command(get_excute_backup_others_command)

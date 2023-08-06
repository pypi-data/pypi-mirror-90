#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import stat
import time
import threading
import time
from git import Repo
import shutil

from xyscript.common.xylog import *
from xyscript.ios.cert import Cert
from xyscript.ios.CommonScript import IOSProjectTool
import xyscript.common.globalvar as gv
from xyscript.ios.iosProjectTool import IOSTool
from xyscript.config import Config
from xyscript.common.file import File
from xyscript.ios.gitandjira import GitLab

SELECT_FILE_COUNT = 0
WORK_SPACE = None
ENV_CHANGE_COUNT = 0
UPLOAD_TESTFLIGHT_COUNT = 1


class Package:
    
    def clone_form_address(self,address,local_path,project_folder_name):

        from pathlib import Path
        folder_name = ""
        if project_folder_name == None:
            folder_name = (address.split("/")[-1]).split(".")[0] +'_' + time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))
        else:
            folder_name = project_folder_name
        # folder_name = (address.split("/")[-1]).split(".")[0] +'_' + time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time()))

        try:
            #创建目录
            local_path = local_path + "/" + folder_name
            if Path(local_path).exists():
                warninglog(folder_name + "is exists")
            else:
                os.mkdir(local_path)
            
            try:
                os.chdir(local_path)
                warninglog("current workspace is: " + local_path)
            except BaseException as error:
                faillog("change worksapce failed")
                # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                sys.exit()
                
            # 更改权限
            os.chmod(local_path, stat.S_IRWXU)
            local_path = local_path + "/"
            Repo.clone_from(url=address, to_path=local_path, progress=None)
            successlog("clone project success")
        except BaseException as error:
            warninglog(format(error))

    def change_branch(self, branch_name, git=None):
        """
        change_branch
        """
        if git is None:
            repo = Repo(os.getcwd())
            # 更新远端分支列表
            repo.git.remote('update','origin','--prune')
            # print(os.getcwd())
            print("start change branch to:",branch_name)
            local_branch_names = []#本地库列表
            remote_branch_names = []#远端库列表
            current_branch = repo.active_branch.name
            # print("current_branch_name:", current_branch)
            for localitem in repo.heads :
                local_branch_names.append(localitem.name)
                # print(localitem.name)
            # print("local_branch_names:", local_branch_names)

            for remoteitem in repo.refs:
                remote_branch_names.append(remoteitem.name)
                # print(remoteitem)
            # print("remote_branch_names:", remote_branch_names)

            if branch_name == current_branch:
                # print("就是当前分支，不需要切换")
                warningstring = "current branch is already :" + branch_name
                warninglog(warningstring)
            else:
                if branch_name in local_branch_names:
                    # print("本地存在目标分支，切换即可")
                    try:
                        local_target_branch = None
                        if branch_name == "develop":
                            local_target_branch = repo.heads.develop
                        elif branch_name == "Develop" :
                            local_target_branch = repo.heads.Develop
                        elif branch_name == "master" :
                            local_target_branch = repo.heads.master
                        else:
                            local_target_branch = repo.heads[branch_name]

                        repo.head.reference = local_target_branch
                        successlog("change branch success")
                    except BaseException as error:
                        errstr = "change branch failed:" + str(error)
                        faillog(errstr)
                        # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                        sys.exit()
                    
                else:
                    remote_branch_name = 'origin/' + branch_name
                    if remote_branch_name in remote_branch_names:
                        # print("远端存在目标分支同名分支，checkout")
                        try:
                            git = repo.git
                            git.checkout('-b', branch_name, remote_branch_name)
                            # repo.remote().pull()
                            successlog("change branch success")
                        except BaseException as error:
                            errstr = "checkout failed:" + str(error)
                            faillog(errstr)
                    else:
                        show_tag = repo.git.show(branch_name)
                        if 'commit' in show_tag and 'Author:' in show_tag and 'Date:' in show_tag:
                            # 不是分支，是tag
                            try:
                                printandresult('git fetch origin tag ' + branch_name)
                                successlog("change tag success")
                            except BaseException  as error:
                                errstr = "checkout tag failed:" + str(error)
                                faillog(errstr)
                        else:
                            errstr = "have no branch named:" + branch_name + " exist,cannot to checkout"
                            # errstr = "\033[1;31m" + "远端不存在名为："+ branch_name + "的分支，无法checkout,请先创建远端仓库分支再checkout" + "\033[0m"
                            faillog(errstr)
                            # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                            sys.exit()

        else:
            print(branch_name)

    def pull_submodule(self,ignore_assets=False):
        """
        pull submodules
        """
        current_submodule = None
        try:
            currentPath = os.getcwd()
            repo = Repo(currentPath)
            initFlag = 0
            file = open("ProjConfig.json")
            moduleConfigList = json.load(file)
            rn_module_path = None
            for moduleConfig in moduleConfigList:
                module_path = currentPath + "/" + moduleConfig["module"]
                if moduleConfig["module"] == "submodules/module-rn":
                    rn_module_path = module_path
                if not os.listdir(module_path):
                    initFlag = 1
            if initFlag == 1:
                print("submodule init...")
                repo.git.submodule('update', '--init')
                successlog("submodule init success")
            copy_assets_path = os.getcwd() + '/' + 'image.json'
            have_copy_assets_sh = os.path.exists(copy_assets_path)
            for moduleConfig in moduleConfigList:
                current_submodule = moduleConfig["module"]
                module_path = currentPath + "/" + moduleConfig["module"]
                sub_repo = Repo(module_path)
                sub_remote = sub_repo.remote()
                sub_repo.git.remote('update','origin','--prune')
                sub_repo.git.reset('--hard')

                branch = ""
                bracnh_name = ""

                ignore_assets_path = self.is_key_in_json(current_submodule,copy_assets_path)
                if ignore_assets and have_copy_assets_sh and (ignore_assets_path is not None):
                    sub_repo.git.clean('-df',ignore_assets_path)
                    print('已忽略资源文件夹：' + ignore_assets_path)
                if "branch" in moduleConfig.keys():
                    branch = "\tbranch"
                    bracnh_name = "\t" + moduleConfig["branch"]
                    sub_repo.git.checkout(moduleConfig["branch"])
                elif "commit" in moduleConfig.keys():
                    branch = "\tcommit"
                    bracnh_name = "\t" + moduleConfig["commit"]
                    sub_repo.git.checkout(moduleConfig["commit"])
                elif "tag" in moduleConfig.keys():
                    branch = "\ttag"
                    bracnh_name = "\t" + moduleConfig["tag"]
                    sub_repo.git.checkout(moduleConfig["tag"])
                sub_remote.pull()
                string = "\t" + moduleConfig["module"] + logitem().successitem(bracnh_name) + " of " + logitem().successitem(branch) + " \tpull success"
                print(string)

                # 针对rn模块
            if rn_module_path is not None:
                warninglog("start setup rn module...")
                self.check_node_env()
                # 切换到rn模块目录
                os.chdir(rn_module_path)
                rn_ios_shell_path = rn_module_path + '/rn_ios'
                if os.path.isfile(rn_ios_shell_path):
                    printandresult(rn_ios_shell_path)
                else:
                    printandresult("npm install")
                    printandresult('npm install scheduler  --save')
                    printandresult("rm -rf bundle")
                    printandresult("mkdir bundle")
                    printandresult("node node_modules/react-native/local-cli/cli.js bundle --entry-file index.js  --platform ios --dev false --bundle-output bundle/index.jsbundle --assets-dest bundle")
                successlog("setup rn module success!")
                # 切回原目录
                os.chdir(currentPath)
                successlog("restore workspace success!")
        except BaseException as error:
            if current_submodule is not None:
                submodule_error = "pull " + current_submodule + " failed"
                faillog(submodule_error)
            errorstr = "pull submodule failed:" + format(error)
            faillog(errorstr)
            # sys.exit()
    def is_key_in_json(self,key,file):
        assets_path = None
        with open(file,'r',encoding='utf8')as fp:
            json_data = json.load(fp)
            assets_list = json_data['imageList']
            for assets_item in assets_list:
                if key in assets_item['image']:
                    path = assets_item['assets']
                    assets_path = path.split(key)[1][1:] + '/'
                    break
        return assets_path

    def check_node_env(self):
        warninglog("start check node environment")
        result = printandresult('node -v')
        if 'node: command not found' in result:
            printandresult('brew install node')

    def run_extension_sh(self,file_list):
        for file in file_list:
            file_path = os.getcwd() + '/' + file
            if os.path.exists(file_path):
                warninglog("执行文件：" + file_path)
                printandresult("sh " + file_path)

    def change_default_net_env(self,env):
        global ENV_CHANGE_COUNT
        filepath = self._search_xcodeproj() + "/project.pbxproj"
        print("start change default environment variable")
        file_data = ""
        try:
            with open(filepath,encoding="utf-8") as f:
                for line in f:
                    if "SC_URL_TYPE =" in line:
                        # print(line,end="")
                        line = str.split(line,'SC_URL_TYPE')[0] + "SC_URL_TYPE = " + env +";\n"
                    file_data += line

            with open(filepath,"w",encoding="utf-8") as f:
                f.write(file_data)
            successlog("change " + env +" environment success")   
        except BaseException  as error:
            faillog("change " + env +" environment failed:" + format(error))
        
    def _just_for_uploadbugly(self):
        filepath = self._search_xcodeproj() + "/project.pbxproj"
        print("start add build setting for upload bugly")
        file_data = ""
        try:
            with open(filepath,encoding="utf-8") as f:
                for line in f:
                    add_line = ""
                    if "SC_URL_TYPE =" in line:
                        add_line = str.split(line,'SC_URL_TYPE')[0] + "SC_BUGLY_DEFAULT = default;\n"
                    file_data += line 
                    file_data += add_line
            with open(filepath,"w",encoding="utf-8") as f:
                f.write(file_data) 
            successlog("add build setting for upload bugly success")
        except BaseException  as error:
            faillog("add build setting for upload bugly failed:" + format(error))

        
    def _search_xcodeproj(self):
        paths = os.listdir(os.getcwd())
        for filename in paths:
            if ".xcodeproj" in filename :
                return filename
        faillog("The current path does not have a: xcodeproj file,such as :projectname.xcodeproj")
        # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
        sys.exit()

    def _add_empty_file(self,fileName="package_empty_file"):
        f= open(fileName,"w")
        f.close
    
    def _pull_lastest_code(self,branch):
        currentPath = os.getcwd()
        repo = Repo(currentPath)
        repo.git.checkout(branch)
        file = open("ProjConfig.json")
        moduleConfigList = json.load(file)
        print("pull " + logitem().successitem("shell") + " in branch " + logitem().successitem(branch) + " success")
        repo.git.pull()
        for moduleConfig in moduleConfigList:
            module_path = currentPath + "/" + moduleConfig["module"]
            sub_repo = Repo(module_path)
            sub_repo.git.checkout(moduleConfig["branch"])
            sub_repo.git.pull()
            print("pull " + logitem().successitem(moduleConfig["module"]) + " in shell " + logitem().successitem(branch) + " success")

    def _get_current_config_file(self):
        file = open("ProjConfig.json")
        moduleConfigList = json.load(file)
        return moduleConfigList

    def _clear_local_workspace(self,date):
        currentPath = os.getcwd()
        repo = Repo(currentPath)
        repo.git.reset('--hard')#清空壳工程本地工作空间
        for moduleConfig in date:
            module_path = currentPath + "/" + moduleConfig["module"]
            sub_repo = Repo(module_path)
            sub_repo.git.reset('--hard')
        print(logitem().successitem("clear local workspace success"))

    def add_tag_after_package(self,tag):
        try:
            if tag is not None:
                currentPath = os.getcwd()
                repo = Repo(currentPath)
                if tag not in repo.git.tag():
                    repo.git.tag(tag)
                    repo.git.push('origin',tag)
                    successlog("add tag to shell success")
                    #子模块添加tag
                    currentPath = os.getcwd()
                    file = open("ProjConfig.json")
                    moduleConfigList = json.load(file)
                    for moduleConfig in moduleConfigList:
                        module_path = currentPath + "/" + moduleConfig["module"]
                        sub_module = Repo(module_path)
                        sub_module.git.tag(tag)
                        sub_module.git.push('origin',tag)
                        successlog("add tag to " + moduleConfig["module"] + " success")
                else:
                    warninglog("tag named: " + tag + " is exists!")
        except BaseException as error:
            faillog("add tag failed:" + format(error))

    def cache_symbol_at_home(self,path):
        #复制符号表到本地
        try:
            root_path = Config().get_sys_root_path()
            sym_path = "symbol/"
            cache_path = root_path + Config().get_config("File-store-path","cache_path") + sym_path + path
            File().creat_folder(cache_path)
            folder_name = os.getcwd()
            files = File().find_files_contain(folder_name,".app.dSYM.zip")
            if len(files) > 0:
                for file in files:
                    shutil.copy(file,cache_path)
                successlog("cache symbol files success")
            else:
                warninglog("have no symbol need to cache")
        except BaseException as error:
            faillog("cache symbol failed:" + format(error))

    def handle_package_order(self,order_array=None,project_version=None, project_build=None, env=None):
        failed_platform = []
        for index, platform_name in enumerate(order_array):
            shell_str = "fastlane package" + platform_name + project_version + project_build + env
            result = self._platform_package(shell_str)
            if index != len(order_array) -1:
                IOSTool().add_content_to_file("AppDelegate.h")
            if result == False:
                failed_platform.append(platform_name)
        
        if len(failed_platform) > 0:
            faillog("package to all failed")
        else:
            successlog("package to all success")

    def _platform_package(self,shell_str):
        global UPLOAD_TESTFLIGHT_COUNT
        text = printandresult(shell_str)
        if "fastlane.tools just saved" in text or "fastlane.tools finished successfully" in text:
            UPLOAD_TESTFLIGHT_COUNT = 1
            return True 
        elif (("An error occurred while uploading the package" in text) 
                or ("An error occurred while uploading the file" in text) 
                or ("Error uploading ipa file, for more information see above" in text) 
                or ("fastlane finished with errors" in text) 
                or ("Error building the application - see the log above" in text)):
            if UPLOAD_TESTFLIGHT_COUNT < 3:
                faillog("upload to testflight failed " + str(UPLOAD_TESTFLIGHT_COUNT) + " times")
                UPLOAD_TESTFLIGHT_COUNT = UPLOAD_TESTFLIGHT_COUNT +1
                warninglog("start uploading " + str(UPLOAD_TESTFLIGHT_COUNT) + " time")
                shell_str1 = shell_str
                if "packagetestflight2" not in shell_str:
                    shell_str1 = shell_str.replace("packagetestflight","packagetestflight2")
                return self._platform_package(shell_str1)
            else:
                UPLOAD_TESTFLIGHT_COUNT = 1
                return False
        else:
            UPLOAD_TESTFLIGHT_COUNT = 1
            return False


    def package_to_platform(self,platform=None, project_version=None, project_build=None, emails=None, env=None,package_order=None):
        """
        配置证书 等效于 fastlane + platform
        """
        #获取项目当前version、build

        if platform == None:
            platform = "pgyer"
            
        version_str = ""
        build_str = ""
        env_str = ""
        if project_version != None:
            version_str = " version:" + project_version
        
        if project_build != None:
            build_str = " build:" + project_build

        if env != None:
            env_str = " env:" + env

        
        print("start package to " + platform)
        if Cert().fastlane_is_in_gem() or Cert().fastlane_is_in_brew() :
            shell_str = "fastlane package" + platform + version_str + build_str + env_str
            try:
                if Cert()._have_fastfile():
                    if platform == "all":#分开打包防止多次打包结果相互影响

                        if package_order == None or package_order == "0":
                            self.handle_package_order(["testflight","pgyer"],version_str,build_str,env_str)
                        elif package_order == "1":
                            self.handle_package_order(["pgyer","testflight"],version_str,build_str,env_str)
                        else:
                            faillog("nonsupport package_order")
                    else:
                        result = self._platform_package(shell_str)
                        if result:
                            successlog("package to " + platform + " success")
                        else:
                            faillog("package to " + platform + " failed")

                else:
                    faillog("You may not have the fastfile,please set fastlane up first!")
                    sys.exit()
                
            except BaseException  as error:
                faillog(str(error))
                sys.exit()
        else:
            warninglog("You may not have the fastlane installed yet,autoinstall now...")
            Cert()._install_fastlane()
            self.package_to_platform(platform,project_version,project_build,env=env)
    

    def auto_package(self, project_address=None, branch_name=None, platform=None, net_env=None, project_version=None, project_build=None,emails=None,tag_name=None,package_order=None,package_folder=None):
        if branch_name == None:
            branch_name = "Develop"
        if platform == None:
            platform = "pgyer"
        if emails == None:
            emails = []

        print("自动打包\n项目：",project_address,"\n分支为：",branch_name,"\n发布平台为：",platform,"\n网络环境：",net_env,"\n版本号：",project_version,"\n编译号：",project_build)
        # print("please choose an folder")
        
        # clone
        # self.clone_form_address(project_address,self.select_directory())
        self.clone_form_address(project_address,os.getcwd(),package_folder)
        # 切换分支
        self.change_branch(branch_name)
        # 拉子模块
        self.pull_submodule()
        # pod indtall
        IOSProjectTool().run_pod_install()
        # 选择网络环境
        if net_env != None:
            self.change_default_net_env(net_env)
        # #fastlane syn
        # Cert().run_cert_syn()
        # #安装 pgyer 插件
        os.system("bundle install")
        # #打包
        self.package_to_platform(platform, project_version, project_build,emails,env=net_env,package_order=package_order)
        # 打tag
        self.add_tag_after_package(tag_name)
        # 缓存symbol
        path = os.getcwd().split("/")[-1]
        Package().cache_symbol_at_home(path)

    def merge_code(self,code_branch,package_branch,email,url=None,keyword=None):
        """
        合并代码(开发分支名、打包分支名)
        """
        if code_branch == None:
            code_branch = "Develop"
        if package_branch == None:
            package_branch = "zuche-test"

        try:
            self.change_branch(code_branch)
            currentPath = os.getcwd()
            repo = Repo(currentPath)
            moduleConfigList = self._get_current_config_file()
            # 清空本地工作空间
            self._clear_local_workspace(moduleConfigList)
            # 检出 code_branch 分支的最新代码
            self._pull_lastest_code(code_branch)
            codebranch_config = self._get_current_config_file()
            # 检出 package_branch 分支的最新代码
            self._pull_lastest_code(package_branch)
            # 合并 code_branch 分支到当前 package_branch 分支
            for moduleConfig in codebranch_config:
                module_path = currentPath + "/" + moduleConfig["module"]
                sub_repo = Repo(module_path)
                merge_str = "merge " + moduleConfig["branch"] + " into " + package_branch
                sub_repo.git.merge(moduleConfig["branch"],'-m', merge_str, '--log=10')
                print("merge " + logitem().successitem(moduleConfig["module"]) + " success")
            repo = Repo(currentPath)
            merge_str = "merge " + code_branch + " into " + package_branch
            repo.git.merge(code_branch, '-m', merge_str ,'--log=10')
            print("merge "+ logitem().successitem("shell") + " from " + logitem().successitem(code_branch) + " to " + logitem().successitem(package_branch) + " success")
            # repo.git.commit('-a', '-m', merge_str)

            #推远端
            repo.git.push()
            print("push " + logitem().successitem("shell") + " success")
            date = self._get_current_config_file()
            for moduleConfig in date:
                module_path = currentPath + "/" + moduleConfig["module"]
                sub_repo = Repo(module_path)
                sub_repo.git.push()
                print("push " + logitem().successitem(moduleConfig["module"]) + " success")
            
            # 还原到原始分支

            # 发送邮件给相关人员
            if email is not None:
                GitLab().get_all_commit_between_push(code_branch=code_branch,package_branch=package_branch,workspace=currentPath,mail=email,url=url,keyword=keyword)

        except BaseException as error:
            errorstr = "merge failed:" + format(error)
            faillog(errorstr)
            # sys.exit()


    def init_project(self, project_address=None, branch_name=None, platform=None, net_env=None):
        if branch_name == None:
            branch_name = "Develop"
        if platform == None:
            platform = "pgyer"

        print("initial 项目：",project_address," 分支为：",branch_name," 发布平台为：",platform,"网络环境：",net_env)
        print("please choose an folder")
        
        # #clone
        # self.clone_form_address(project_address,self.select_directory())
        # #切换分支
        self.change_branch(branch_name)
        # #拉子模块
        self.pull_submodule()
        # #pod indtall
        IOSProjectTool().run_pod_install()
        # #选择网络环境
        if net_env != None:
            self.change_default_net_env(net_env)
        # #fastlane syn
        Cert().run_cert_syn()

if __name__ == "__main__":
    # pass
    # Package().change_default_net_env("dev")
    # Package()._get_project_version()
    # Package().merge_code("Develop","zuche-test")
    # Package()._add_empty_file()
    # Package()._just_for_uploadbugly()
    # Package().pull_submodule()
    # IOSTool().add_content_to_file("AppDelegate.h")
    # Package().add_tag_after_package("tag_03")
    # path = os.getcwd().split("/")[-1]
    # Package().cache_symbol_at_home(path)
    # path = '/Users/v-sunweiwei/Desktop/saic/sam
    
    # print(Package().check_node_env())

    # path = '/Users/v-sunweiwei/Desktop/saic/ios-shell-passenger'
    # os.chdir(path)
    # repo = Repo(path)
    # printandresult('git ls-remote --tags origin')
    # printandresult('git show SRP_28722')
    # print('Author:' in repo.git.show('SRP_2872'))

    # Package().run_extension_sh(['branchS.sh'])
    # Package().is_key_in_json('submodules/module-login','/Users/sunweiwei/Desktop/Project/ios-shell-driver-cz/image.json')
     Package().pull_submodule(True)


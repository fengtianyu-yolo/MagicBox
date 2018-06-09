#! /usr/local/bin/python3
# -*- coding=utf-8 -*-

import json
import requests
from subprocess import check_output


class GitApi:
    @staticmethod
    def get_commit_msg():
        """
        获取最近的提交信息
        """
        return check_output("git log --pretty='%s' -n 1", shell=True).decode().replace('\n', '')

    @staticmethod
    def get_current_branch_name():
        """
        获取当前所在分支的分支名
        """
        return check_output('git symbolic-ref --short HEAD', shell=True).decode().replace('\n', '')

    @staticmethod
    def get_current_repo_name():
        """
        获取当前项目的group名和project名 (groupname, projectname)
        """
        # 获取pushurl地址 如 Push  URL: git@172.28.6.24:ios_phenix/tcontentCommon.git
        full_path = check_output("git remote show origin | grep -i 'push  url'", shell=True).decode()
        # 以':'分隔 取最后一个 得到 ios_phenix/tcontentCommon.git
        url_path = full_path.split(':')[-1]
        # 去掉.git ios_phenix/tcontentCommon
        full_name = url_path[:-5]
        # 以'/'分割
        return tuple(full_name.split('/'))


class GitLabApi:
    pass

    def __init__(self):
        with open('/Users/fengtianyu/MySpace/Scripts/gitlab-config.json', 'r') as f:
            content = f.read()
            self._config = json.loads(content)
            self._host = self._config['host']
            self._base_url = 'http://' + self._host + '/api/v4/'

            header = self._config['Private-Token']
            self._header = {
                'Private-Token': header
            }
        session = requests.Session()
        self._session = session

    def create_mr(self):
        # 获取被merge分支
        target_branch = self._config['target_branch']

        # 提交记录作为title
        commit_msg = GitApi.get_commit_msg()

        # 获取project_id 配置表有则取配置表中的 没有
        names = GitApi.get_current_repo_name()
        group_name = names[0]
        project_name = names[-1]
        project_id = self.get_project_id_by_name(project_name)

        # 获取当前所在分支
        source_branch = GitApi.get_current_branch_name()
        # 如果当前在develop或release分支 获取上次提交到的分支
        if source_branch == 'develop' or source_branch == 'release':
            merge_info = self.get_branches(project_id)
            commit_msg = merge_info[0]
            source_branch = merge_info[1]

        # 获取审核人id
        assignee_id = self._config['assignee_id']

        # 构造请求数据
        data = {
            'title': commit_msg,
            'id': project_id,
            'source_branch': source_branch,
            'target_branch': target_branch,
            'assignee_id': assignee_id,
            'remove_source_branch': '1'
        }

        # 拼接url
        url = self._base_url + 'projects/' + str(project_id) + '/merge_requests'
        print('url=' + url)
        #print(self._header)
        print(data)

        # 发起请求
        response = self._session.post(url=url, headers=self._header, data=data).text
        print('结果\n' + response)

    def get_project_id_by_name(self, project_name):
        if project_name in self._config:
            return self._config[project_name]
        else:
            return self.query_projectid_by_name(project_name)

    def query_projectid_by_name(self, project_name):
        """
        根据项目名查询项目id
        """
        query_url = self._base_url + 'projects?search=' + project_name
        response = self._session.get(url=query_url, headers=self._header)
        projects = json.loads(response.text)
        print('默认配置表中没有找到当前库，搜索到%d个库' % len(projects))
        index = 0
        for project in projects:
            print('%d 库名:%s' % (index , project['name']))
            index += 1

        select_index = input('选择库：')
        select_index = int(select_index)
        project = projects[select_index]
        return project['id']

    def search_user_id_by_name(self, name):
        """
        根据用户名查询用户id
        """
        query_url = self._base_url + '/users?search=' + name
        response = self._session.get(query_url).text
        users_list = json.loads(response)

    def get_branches(self, project_id):
        """
        获取当前库的所有远端分支，过滤保护的分支和已经merge的分支
        """
        query_url = self._base_url + 'projects/' + str(project_id) + '/repository/branches'
        response = self._session.get(url=query_url, headers=self._header)
        branches = json.loads(response.text)

        index = 0
        for branch_info in branches:
            branch_name = branch_info['name']
            merged = branch_info['merged']
            protected = branch_info['protected']
            if not merged and not protected:
                print('index:%d 分支：%s' %( index, branch_name))
            index += 1

        select_index = input('选择分支:')
        select_index = int(select_index)
        select_branch = branches[select_index]
        name = select_branch['name']
        title = select_branch['commit']['title']
        return (title, name)
        

    def __str__(self):
        return 'base_url:' + self._base_url


if __name__ == '__main__':
    api = GitLabApi()
    # api.query_projectid_by_name('common')
    api.create_mr()



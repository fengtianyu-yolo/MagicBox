from subprocess import check_output
import sys

class GitApi:
    @staticmethod
    def fast_push():
        """
        快速执行 git add . git commit -m msg git push origin branch
        提交到远端的当前分支
        """
        # 添加到暂存区
        check_output('git add .', shell=True)

        # 获取提交信息
        commit_msg = sys.argv[1]
        print(commit_msg)
        commit_command = "git commit -m \"" + commit_msg + "\""
        check_output(commit_command, shell=True)

        # 获取当前所在分支
        branch_name = check_output('git symbolic-ref --short HEAD', shell=True).decode().replace('\n', '')
        push_command = 'git push origin ' + branch_name
        check_output(push_command, shell=True)



if __name__ == '__main__':
    GitApi.fast_push()



import requests
import json
import threading

class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class ScrapydManage(metaclass=SingletonType):

    def add_spider(self, hostname, project, version, eggfile):
        """
        添加一个爬虫项目
        :param hostname: host:port 主机地址:端口
        :param project: 项目名(如果项目不存在，将会创建)
        :param version: 版本号
        :param eggfile: egg文件 eg:open('file.egg','rb').read()
        :return: dict eg:{'node_name': 'JD', 'project': 'wubahouse', 'version': 'r1', 'spiders': 3, 'status': 'ok'}
        """
        data = {
            'project': project,
            'version': version
        }
        return self.__get_source('http://%s/addversion.json' % hostname, 'post', data, eggfile)

    def get_server_status(self, hostname):
        """
        获取服务器状态
        :param hostname: host:port 主机地址:端口
        :return: dict eg:{'status': 'ok', 'running': 0, 'finished': 0, 'pending': 0, 'node_name': 'JD'}
        """
        return self.__get_source('http://%s/daemonstatus.json' % hostname, 'get')

    def get_project_list(self, hostname):
        """
        获取服务器上的项目列表
        :param hostname: host:port 主机地址:端口
        :return: dict eg:{'node_name': 'JD', 'projects': ['wubahouse'], 'status': 'ok'}
        """
        return self.__get_source('http://{}/listprojects.json'.format(hostname), 'get')

    def get_spider_list(self, hostname, project, version=None):
        """
        获取爬虫列表
        :param hostname: host:port 主机地址:端口
        :param project:  项目名称
        :param version:  版本号(可选)
        :return: dict eg:{'node_name': 'JD', 'spiders': ['ppgyspider', 'xiaoqu', 'zufang'], 'status': 'ok'}
        """
        if version:
            api_url = 'http://{}/listspiders.json?project={}&_version={}'.format(hostname, project, version)
        else:
            api_url = 'http://{}/listspiders.json?project={}'.format(hostname, project)
        return self.__get_source(api_url, 'get')

    def get_project_version_list(self, hostname, project):
        """
        获取项目的历史版本
        :param hostname: host:port 主机地址:端口
        :param project: 项目名称
        :return: dict eg:{'node_name': 'JD', 'versions': ['r1'], 'status': 'ok'}
        """
        return self.__get_source('http://{}/listversions.json?project={}'.format(hostname, project), 'get')

    def get_job_list(self, hostname, project):
        """
        获取项目的任务列表
        :param hostname: host:port 主机地址:端口
        :param project:  项目名称
        :return: dict eg:{'running': [], 'node_name': 'JD', 'finished': [], 'pending': [], 'status': 'ok'}
        """
        return self.__get_source('http://{}/listjobs.json?project={}'.format(hostname, project), 'get')

    def del_version(self, hostname, project, version):
        """
        删除项目的一个版本
        :param hostname: host:port 主机地址:端口
        :param project: 项目名称
        :param version: 版本名称
        :return: dict eg:{'node_name': 'JD', 'status': 'ok'}
        """
        data = {
            'project': project,
            'version': version
        }
        return self.__get_source('http://{}/delversion.json'.format(hostname), 'post', data)

    def del_project(self, hostname, project):
        """
        删除一个项目
        :param hostname: host:port 主机地址:端口
        :param project:  项目名称
        :return: dict eg:{'node_name': 'JD', 'message': "No such file or directory: 'eggs'", 'status': 'error'}
        """
        return self.__get_source('http://{}/delproject.json'.format(hostname), 'post', data={'project': project})

    def start_job(self, hostname, project, spider, setting=None, jobid=None, version=None, args=None):
        """
        开始一个任务
        :param hostname: host:port 主机地址:端口
        :param project: 项目名
        :param spider:  爬虫名
        :param setting: 设置(可选)
        :param jobid:   任务id 未设置会自动生成(可选)
        :param version: 版本号(可选)
        :param args: dict 参数(可选)
        :return: dict eg:
        """
        if not args:
            args = {}
        api_url = 'http://{}/schedule.json'.format(hostname)
        data = {
            'project': project,
            'spider': spider,
            'setting': setting,
            'jobid': jobid,
            'version': version,
        }
        for item in args.items():
            data[item[0]] = item[1]
        data1 = {}
        for item in data.items():
            if item[1]:
                data1[item[0]] = item[1]
        return self.__get_source(api_url, 'post', data1)

    def __get_source(self, api_url, method, data=None, file=None):
        if method == 'post':
            if file:
                req = requests.post(api_url, data=data, files={'egg': file})
            else:
                req = requests.post(api_url, data=data)
        else:
            req = requests.get(api_url)

        if req.status_code == 200:
            try:
                return json.loads(req.content)
            except Exception as e:
                return {'status': 'error', 'msg': str(e)}
        return {'status': 'error', 'msg': 'response code:{}'.format(req.status_code)}

    def cancel_job(self, hostname, project, jobid):
        """
        取消一个任务
        :param hostname: host:port 主机地址:端口
        :param project: 项目名
        :param jobid: 任务id
        :return: dict eg:{'prevstate': 'running', 'node_name': 'JD', 'status': 'ok'}
        """
        api_url = 'http://{}/cancel.json'.format(hostname)
        data = {
            'project': project,
            'job': jobid
        }
        return self.__get_source(api_url, 'post', data)


if __name__ == "__main__":
    sm = ScrapydManage()
    hostname = '116.196.93.35:6800'
    # 创建一个项目并上传egg文件
    with open('./wubahouse.egg', 'rb') as fp:
        print(sm.add_spider(hostname, 'wubahouse', 'r1', fp.read()))
    print(sm.get_job_list(hostname, 'wubahouse'))
    print(sm.cancel_job(hostname, 'wubahouse', '3cac864a46cf11e8b2e9fa163e279e53'))
    print(sm.start_job(hostname, 'wubahouse', 'ppgyspider',
                       args={'orderno': 'ZF2018498307Tr5TIY', 'secret': 'e1ae925896f8456a9835c4c8873b07b2'}))

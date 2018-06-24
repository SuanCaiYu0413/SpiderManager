# *_*coding:utf-8 *_*
import threading
import uuid
from apscheduler.schedulers.background import BackgroundScheduler


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class CronTab(metaclass=SingletonType):
    __bksch = BackgroundScheduler()
    __jobs = {}

    def star_job(self, task, cron, kwargs=None):
        """
        开始一个任务
        :param task: func 任务方法
        :param cron: dict cron调度字典 eg:{'year':'*','month':'*','day'='*'}
        :param kwargs: dict 任务方法的参数 eg:{'hostname':'xxx.xx.x.x:xxx','project':'wubahouse'}
        :return: 任务id
        """
        if not kwargs:
            args = {}
        else:
            args = kwargs
        job = self.__bksch.add_job(task, cron, kwargs=args)
        jobid = uuid.uuid1()
        self.__jobs[jobid] = job
        return jobid

    def remove_job(self, jobid):
        """
        删除一个任务，删除任务不可恢复
        :param jobid: 需要删除的任务
        :return:
        """
        job = self.__jobs.get(jobid, None)
        if job:
            job.remove()
        else:
            raise Exception()

    def resume_job(self, jobid):
        """
        恢复一个暂停中的任务
        :param jobid: 需要恢复的任务id
        :return:
        """
        job = self.__jobs.get(jobid, None)
        if job:
            job.resume()
        else:
            raise Exception()

    def pause_job(self, jobid):
        """
        暂停一个任务
        :param jobid: 需要暂停的任务id
        :return: None
        """
        job = self.__jobs.get(jobid, None)
        if job:
            job.pause()
        else:
            raise Exception()

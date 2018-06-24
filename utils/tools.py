# @Time    : 2018/6/15 10:18
# @Author  : SuanCaiYu
# @File    : tools
# @Software: PyCharm
import os
import config


def formatSize(bytes):
    """
    格式化文件大小的单位
    :param bytes: int 字节数
    :return: 带单位的文件大小
    """
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


def getDocSize(path):
    """
    获取文件大小
    :param path: 文件路径
    :return: 文件大小的字节数
    """
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        raise err


def get_eggfile_count():
    """
    查询egg文件
    :return: ([{"name":文件名,"size":文件大小},...],文件数量)
    """
    eggdir = config.eggdir
    files = os.listdir(eggdir)
    filenames = []
    count = 0
    for file in files:
        if os.path.isfile('%s%s' % (eggdir, file)):
            filename, ext = os.path.splitext(file)
            if ext == '.egg':
                count += 1
                filenames.append({"name": filename, "size": getDocSize('%s%s' % (eggdir, file))})
    return filenames, count


def del_eggfile(filename):
    """
    删除egg文件
    :param filename: 文件名
    :return: {0:失败,1:成功}
    """
    filepath = os.path.join(config.eggdir, "{}.egg".format(filename))
    if os.path.isfile(filepath):
        try:
            os.remove(filepath)
            return 1
        except Exception as e:
            return 0
    else:
        return 0

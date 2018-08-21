from setuptools import setup, find_packages
import os


def pack():
	os.getcwd()
	os.chdir(r'C:\Users\Administrator\Desktop\test')
	setup(
		name = "xxx",
		version = "0.1",
		packages = find_packages()
		)
		
if __name__ == '__main__':
    pack()
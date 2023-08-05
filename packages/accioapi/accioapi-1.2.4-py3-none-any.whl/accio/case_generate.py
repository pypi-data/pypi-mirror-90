# -*- encoding: utf-8 -*-
"""
@File    : case_generate.py
@Time    : 2020/10/16 10:39
@Author  : liyinlong
@Software: PyCharm
"""

import time
import os


class Generate(object):

    def __init__(self, data, case_name=None):
        self.data = data
        self.case_name = case_name

        #self.root_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
        self.root_path=os.path.join(os.getcwd())
        if not os.path.exists(str(self.root_path) + '\\temp\\Testcase'):
            os.makedirs(str(self.root_path) + '\\temp\\Testcase')

    '''
    依据har文件method信息生成对应case
    如果传入文件名以传入文件名+数据在entries中的位置命名
    不传入文件名默认以path路径命名，截取path后两段命名
    如果没有path路径，以域名命名
    '''

    def case(self):
        list = []
        for t, each in enumerate(self.data):
            list.append(each)
        paths = self.data.get('paths')
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for t, each in enumerate(paths):
            for n, m in enumerate(paths.get(each)):
                method = m          # 取出请求方法
            parameters = paths.get(each).get(method).get('parameters')
            if '{' in each:    # 判断路径里是否有大括号，来拼接response内容
                req = method.lower() + '(host+\"' + each.replace('{', '\"+ ').replace('}', ' +\"')[:-2] + ', params, header)'
            else:
                req = method.lower() + '(host+\"' + each + '\", params, header)'

            each = each.replace('{', '').replace('}', '')
            case_file_name = 'test' + each.replace('/', '_') + '.py'

            key = []
            param_in_paths = []
            param_in_header = []
            if 'securityDefinitions' in list:     # 判断securityDefinitions里是否有参数
                if self.data.get('securityDefinitions'):
                    for a, b in enumerate(self.data.get('securityDefinitions')):
                        if self.data.get('securityDefinitions').get(b).get('name'):
                            in_where = self.data.get('securityDefinitions').get(b).get('in')
                            if in_where == 'body':
                                param_in_paths.append(self.data.get('securityDefinitions').get(b).get('name'))
                                key.append(self.data.get('securityDefinitions').get(b).get('name'))
                            elif in_where == 'header':
                                param_in_header.append(self.data.get('securityDefinitions').get(b).get('name'))
                                key.append(self.data.get('securityDefinitions').get(b).get('name'))
                            else:
                                print("securityDefinitions类型异常")
            dict_param_inpath = ''
            dict_param_inheader = ''
            for num, param in enumerate(parameters):    # 将参数分别放进 params 和 header
                name = param.get('name')
                in_wh = param.get('in')
                key.append(name)
                keys = ', '.join(key)
                if in_wh == 'body':
                    param_in_paths.append(name)
                    dict_param_inpath = str(dict(zip(param_in_paths, param_in_paths))).replace(': \'',': ').replace('\',',',').replace('\'}','}')
                elif in_wh == 'header':
                    param_in_header.append(name)
                    dict_param_inheader = "header.update(" + str(dict(zip(param_in_header, param_in_header))).replace(': \'',': ').replace('\',',',').replace('\'}','}') + ')'
                else:
                    pass
            if dict_param_inpath == '':
                dict_param_inpath = '{}'
            file_write = os.path.join(self.root_path, "TestCase", case_file_name)
            with open(file_write, 'w', encoding="utf-8") as outfile:
                outfile.write("\"\"\"" + "\r")
                outfile.write("@File    : %s" % case_file_name + "\r")
                outfile.write("@Time    : %s" % local_time + "\r")
                outfile.write("@Author  : Automatic generation" + "\r")
                outfile.write("\"\"\"" + "\r")
                outfile.write("#--别名占位" + "\r\r")
                outfile.write("from accio import Http" + "\r\r\r")
                outfile.write("class Case:" + "\r\r")
                outfile.write("\t" + "def __init__(self):" + "\r")
                outfile.write("\t\t" + "self.request = Http.Request()" + "\r\r")
                outfile.write("\t" + "def request_method(self, host, %s, headers):" % keys + "\r")
                outfile.write("\t\t" + "\"\"\"")
                outfile.write("\t\t\t" + "用例描述：数据源文件中第 %s 个request" % str(t+1) + "\r")
                outfile.write("\t\t" + "\"\"\"" + "\r")
                outfile.write("\t\t" + "params = %s" % dict_param_inpath + "\r")
                outfile.write("\t\t" + "header = eval(headers)" + "\r")
                outfile.write("\t\t" + "%s" % dict_param_inheader + "\r")
                outfile.write("\t\t" + "response = self.request.%s" % req + "\r")
                outfile.write("\t\t" + "return response")

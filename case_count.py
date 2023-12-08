import tkinter as tk
from tkinter import filedialog, messagebox
import xmind
import os
from xmindparser import xmind_to_dict


class ParseXmind(object):

    def __init__(self, root):
        self.count = 0
        self.case_fail = 0
        self.case_success = 0
        self.case_block = 0
        self.case_undo = 0
        self.case_priority = 0
        self.case_priority_right = 0
        # total汇总用
        self.total_cases = 0
        self.total_success = 0
        self.total_fail = 0
        self.total_block = 0
        self.total_case_undo = 0
        self.total_case_priority = 0
        self.total_case_priority_right = 0
        # GUI
        root.title('Xmind用例计数器')
        width = 700
        height = 400
        xscreen = root.winfo_screenwidth()
        yscreen = root.winfo_screenheight()
        xmiddle = (xscreen - width) / 2
        ymiddle = (yscreen - height) / 2
        root.geometry('%dx%d+%d+%d' % (width, height, xmiddle, ymiddle))  # 窗口默认大小

        # 2个frame
        self.frm1 = tk.Frame(root)
        self.frm2 = tk.Frame(root)
        #  布局
        self.frm1.grid(row = 1, padx = '100', pady = '10')
        self.frm2.grid(row = 2, padx = '30', pady = '30')

        # self.but_upload = tk.Button(self.frm1, text = '打开xmind文件', command = self.new_lines, bg = '#dfdfdf')
        # self.but_upload = tk.Button(self.frm1, text = '打开xmind文件', command = self.upload_files, bg = '#dfdfdf')
        # self.but_upload.grid(row = 0, column = 0, pady = '10')
        self.text = tk.Text(self.frm1, width = 55, height = 5, bg = '#f0f0f0')
        self.text.grid(row = 1, column = 0)


        self.but2 = tk.Button(self.frm2, text = "打开xmind文件", command = self.upload_files, bg = '#dfdfdf')
        # self.but2 = tk.Button(self.frm2, text = "开始统计", command = self.new_lines, bg = '#dfdfdf')
        self.but2.grid(row = 0, columnspan = 7, pady = '10')
        self.label_file = tk.Label(self.frm2, text = "文件名", relief = 'groove', borderwidth = '2', width = 25,
                                   bg = '#FFD0A2')
        self.label_file.grid(row = 1, column = 0)
        self.label_case = tk.Label(self.frm2, text = "用例数", relief = 'groove', borderwidth = '2', width = 10,
                                   bg = '#FFD0A2').grid(row = 1, column = 1)
        self.label_case_priority = tk.Label(self.frm2, text = "p1", relief = 'groove', borderwidth = '2',
                                            width = 10, bg = '#FFD0A2').grid(row = 1, column = 2)
        self.label_pass = tk.Label(self.frm2, text = "成功", relief = 'groove', borderwidth = '2', width = 10,
                                   bg = '#FFD0A2').grid(row = 1, column = 3)
        self.label_fail = tk.Label(self.frm2, text = "失败", relief = 'groove', borderwidth = '2', width = 10,
                                   bg = '#FFD0A2').grid(row = 1, column = 4)
        self.label_block = tk.Label(self.frm2, text = "阻塞", relief = 'groove', borderwidth = '2', width = 10,
                                    bg = '#FFD0A2').grid(row = 1, column = 5)
        self.label_case_progress = tk.Label(self.frm2, text = "进度", relief = 'groove', borderwidth = '2',
                                            width = 10, bg = '#FFD0A2').grid(row = 1, column = 6)

    def count_case(self, li):
        """
        统计xmind中的用例数
        :param li:
        :return:
        """
        for i in range(len(li)):
            if li[i].__contains__('topics'):  # 带topics标签意味着有子标题，递归执行方法
                self.count_case(li[i]['topics'])
            else:  # 不带topics意味着无子标题，此级别既是用例
                if li[i].__contains__('makers'):  # 有标记成功或失败时会有makers标签
                    for mark in li[i]['makers']:
                        if mark == "c_simbol-right":  # 成功
                            self.case_success += 1
                        elif mark == "c_simbol-wrong":  # 失败
                            self.case_fail += 1
                        elif mark == "symbol-attention":  # 阻塞
                            self.case_block += 1
                        elif mark == "priority-1":  # 优先级
                            self.case_priority += 1
                            if mark == 'c_simbol-right':
                                self.case_priority_right += 1
                self.count += 1  # 用例总数

    def new_line(self, filename, row_number):
        """
        用例统计表新增一行
        :param filename:
        :param row_number:
        :return:
        """

        # 调用python中xmind_to_dict方法,将xmind转成字典
        sheets = xmind_to_dict(filename)  # sheets是一个list，可包含多sheet页；
        for sheet in sheets:
            my_list = sheet['topic']['topics']  # 字典的值sheet['topic']['topics']是一个list
            print(my_list)
            self.count_case(my_list)

        # 插入一行统计数据
        lastname = filename.split('/')
        self.label_file = tk.Label(self.frm2, text = lastname[-1], relief = 'groove', borderwidth = '2', width = 25)
        self.label_file.grid(row = row_number, column = 0)

        self.label_case = tk.Label(self.frm2, text = self.count, relief = 'groove', borderwidth = '2', width = 10)
        self.label_case.grid(row = row_number, column = 1)

        self.label_case_priority = tk.Label(self.frm2, text = self.case_priority, relief = 'groove', borderwidth = '2',
                                            width = 10)
        self.label_case_priority.grid(row = row_number, column = 2)

        self.label_pass = tk.Label(self.frm2, text = self.case_success, relief = 'groove', borderwidth = '2',
                                   width = 10)
        self.label_pass.grid(row = row_number, column = 3)

        self.label_fail = tk.Label(self.frm2, text = self.case_fail, relief = 'groove', borderwidth = '2', width = 10)
        self.label_fail.grid(row = row_number, column = 4)

        self.label_block = tk.Label(self.frm2, text = self.case_block, relief = 'groove', borderwidth = '2', width = 10)
        self.label_block.grid(row = row_number, column = 5)

        # self.label_case_priority = tk.Label(self.frm2, text = "%s/%s" %(self.case_priority_right, self.case_priority), relief = 'groove', borderwidth = '2',
        #                                     width = 15)
        self.label_case_progress = tk.Label(self.frm2, text = "%d%%" %((self.case_success + self.case_fail + self.case_block) * 100/self.count), relief = 'groove', borderwidth = '2', width = 10)
        self.label_case_progress.grid(row = row_number, column = 6)

        self.total_cases += self.count
        self.total_success += self.case_success
        self.total_fail += self.case_fail
        self.total_block += self.case_block
        self.total_case_priority += self.case_priority
        self.total_case_priority_right += self.case_priority_right

    def new_lines(self):
        """
        用例统计表新增多行
        :return:
        """

        lines = self.text.get(1.0, tk.END)  # 从text中获取所有行
        row_number = 2
        for line in lines.splitlines():  # 分隔成每行
            if line == '':
                break
            self.new_line(line, row_number)
            row_number += 1

        # total汇总行
        # self.label_file = tk.Label(self.frm2, text = 'total', relief = 'groove', borderwidth = '2', width = 25)
        # self.label_file.grid(row = row_number, column = 0)
        #
        # self.label_case = tk.Label(self.frm2, text = self.total_cases, relief = 'groove', borderwidth = '2', width = 10)
        # self.label_case.grid(row = row_number, column = 1)
        #
        # self.label_case_priority = tk.Label(self.frm2, text = self.total_case_priority, relief = 'groove',
        #                                     borderwidth = '2', width = 10)
        # self.label_case_priority.grid(row = row_number, column = 2)
        #
        # self.label_pass = tk.Label(self.frm2, text = self.total_success, relief = 'groove', borderwidth = '2',
        #                            width = 10)
        # self.label_pass.grid(row = row_number, column = 3)
        #
        # self.label_fail = tk.Label(self.frm2, text = self.total_fail, relief = 'groove', borderwidth = '2', width = 10)
        # self.label_fail.grid(row = row_number, column = 4)
        #
        # self.label_block = tk.Label(self.frm2, text = self.total_block, relief = 'groove', borderwidth = '2',
        #                             width = 10)
        # self.label_block.grid(row = row_number, column = 5)
        #
        # # self.label_case_priority = tk.Label(self.frm2, text = "%s/%s" %(self.total_case_priority_right, self.total_case_priority), relief = 'groove',
        # #                                     borderwidth = '2', width = 15)
        # self.label_case_progress = tk.Label(self.frm2, text = "%d%%" % ((self.case_success + self.case_fail + self.total_block) * 100 /self.count), relief = 'groove', borderwidth = '2',
        #                             width = 10)
        # self.label_case_progress.grid(row = row_number, column = 6)

    def upload_files(self):
        """
        上传多个文件，并插入text中
        :return:
        """
        select_files = tk.filedialog.askopenfilenames(title = "选择你要统计的xmind用例文件")
        for file in select_files:
            self.text.insert(tk.END, file + '\n')
            self.text.update()
        self.new_lines()

    @staticmethod
    def parse_xmind(path):
        """
        xmind变为一个字典
        :param path:
        :return:
        """
        dic_xmind = xmind_to_dict(path)
        xmind_result = dic_xmind[0]
        return xmind_result

    def create_new_xmind(self, path):
        """
        用原xmind内容新建一个xmind文件
        :param path:
        :return:
        """
        xmind_result = self.parse_xmind(path)
        new_xmind_result = self.dict_result(xmind_result)
        xmind_file = path[:-6].split("/")[-1]
        path_list = path[:-6].split("/")
        path_list.pop(0)
        path_list.pop(-1)
        path_full = "/" + "/".join(path_list)
        new_xmind_file = "{}/{}_new.xmind".format(path_full, xmind_file)
        print(new_xmind_file)
        if os.path.exists(new_xmind_file):
            os.remove(new_xmind_file)
        xmind_wb = xmind.load(new_xmind_file)
        new_xmind_sheet = xmind_wb.getSheets()[0]
        new_xmind_sheet.setTitle(new_xmind_result["sheet_topic_name"])
        root_topic = new_xmind_sheet.getRootTopic()
        root_topic.setTitle(new_xmind_result["sheet_topic_name"])
        for k, v in new_xmind_result["data"].items():
            topic = root_topic.addSubTopic()
            topic.setTitle(k)
            for value in v:
                new_topic = topic.addSubTopic()
                new_topic.setTitle(value)
        xmind.save(xmind_wb)

    def dict_result(self, xmind_result):
        """
        使用原xmind数据构造new_xmind_result
        :param xmind_result:
        :return:
        """
        sheet_name = xmind_result['title']
        sheet_topic_name = xmind_result['topic']['title']  # 中心主题名称
        new_xmind_result = {
            'sheet_name': sheet_name,
            'sheet_topic_name': sheet_topic_name,
            'data': {}
        }
        title_list = []
        for i in xmind_result['topic']['topics']:
            title_temp = i['title']
            title_list.append(title_temp)
            result_list = self.chain_data(i)
            new_xmind_result['data'][title_temp] = result_list
        return new_xmind_result

    @staticmethod
    def chain_data(data):
        """
        原xmind的所有topic连接成一个topic
        :param data:
        :return:
        """
        new_xmind_result = []

        def calculate(s, prefix):
            prefix += s['title'] + '->'
            for t in s.get('topics', []):
                s1 = calculate(t, prefix)
                if s1 is not None:
                    new_xmind_result.append(s1.strip('->'))
            if not s.get('topics', []):
                return prefix

        calculate(data, '')
        return new_xmind_result


if __name__ == '__main__':
    root = tk.Tk()
    ParseXmind(root)
    root.mainloop()
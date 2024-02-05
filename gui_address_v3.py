import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTextEdit
import requests
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP查询工具")
        self.resize(300, 400)

        # 创建布局管理器和中心部件
        layout = QVBoxLayout()
        center_widget = QWidget()

        # 创建控件
        label = QLabel("请输入IP地址:（可以查询多个，以空格分割）")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("请输入要查询的IP地址，例如：153.3.238.110")
        self.button = QPushButton("查询", self)
        self.output_box = QTextEdit()

        # 将控件添加到布局管理器中
        layout.addWidget(label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.button)
        layout.addWidget(self.output_box)

        # 设置中心部件和布局管理器
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)

        # 连接按钮的点击事件
        self.button.clicked.connect(self.on_button_click)
        # 绑定回车查询
        self.input_box.returnPressed.connect(self.on_button_click)

    def on_button_click(self):
        ip_addresses = self.input_box.text().split()  # 以空格分隔多个IP地址
        self.output_box.clear()  # 清空输出框
        for ip_address in ip_addresses:
            if not self.check_ip_format(ip_address):
                self.output_box.append(f"请输入正确的IPv4地址！")
                continue
            ip_info = self.get_ip_info(ip_address)
            self.output_box.append(f"IP地址：{ip_address}")
            try:
                old1 = "\n上报纠错"
                old2 = "上报纠错"
                self.output_box.append(f"归属地：{ip_info['归属地'].replace(old1, '').replace(old2, '')}")
                # print(ip_info)
            except:
                self.output_box.append(f"归属地：none")
            try:
                self.output_box.append(f"运营商：{ip_info['运营商']}")
            except:
                self.output_box.append(f"运营商：none")
            try:
                self.output_box.append(f"IP类型：{ip_info['iP类型']}")
            except:
                self.output_box.append(f"IP类型：none")
            self.output_box.append("")
            # 闪烁查询按钮
            # 生成随机颜色值，排除黑色
            color = "#{:06x}".format(random.randint(0x000001, 0xFFFFFF))
            # 设置查询按钮的样式
            self.button.setStyleSheet(f"background-color: {color}")
            self.button.repaint()
            QApplication.processEvents()

    def check_ip_format(self, ip_address):
        """
        检查IP地址格式是否符合IPv4规范
        """
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or int(part) < 0 or int(part) > 255:
                return False
        return True

    def get_ip_info(self, ip_address):
        cookies = {
            'PHPSESSID': 'h6913r7top2buo88tm3p4pf85o',
            'Hm_lvt_c375abc2df71accdca3ace57d488f925': '1702893254',
            'Hm_lpvt_c375abc2df71accdca3ace57d488f925': '1705485078',
            '__gads': 'ID=9b596806c4066226-22a39bcb7fe500f3:T=1699352012:RT=1705485079:S=ALNI_MbTOmp36O1iIaR0QAAKW7SRqiKpqQ',
            '__gpi': 'UID=00000c8187e3aa73:T=1699352012:RT=1705485079:S=ALNI_MaGHGvFp95ZZ9fPC-O0NEJMX4qKPg',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'sec-ch-ua': '^\\^Not_A',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '^\\^Windows^\\^',
        }

        response = requests.get(f'https://www.ipshudi.com/{ip_address}', headers=headers, cookies=cookies)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        rows = table.find_all('tr')

        ip_info = {}
        for row in rows:
            cells = row.find_all('td')
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            ip_info[key] = value

        return ip_info


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

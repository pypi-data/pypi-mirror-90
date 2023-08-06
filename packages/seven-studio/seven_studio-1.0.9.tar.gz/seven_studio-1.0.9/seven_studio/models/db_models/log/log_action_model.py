
#此文件由rigger自动生成
from seven_framework.mysql import MySQLHelper
from seven_framework.base_model import *


class LogActionModel(BaseModel):
    def __init__(self, db_connect_key='db_sevenstudio', sub_table=None, db_transaction=None):
        super(LogActionModel, self).__init__(LogAction, sub_table)
        self.db = MySQLHelper(config.get_value(db_connect_key))
        self.db_connect_key = db_connect_key
        self.db_transaction = db_transaction

    #方法扩展请继承此类
    
class LogAction:

    def __init__(self):
        super(LogAction, self).__init__()
        self.id = 0  # 自增主键
        self.module_code = ""  # 模块名称
        self.user_id = 0  # 用户id
        self.content = ""  # 日志内容
        self.record_time = 0  # 记录时间
        self.client_ip = ""  # 客户端IP

    @classmethod
    def get_field_list(self):
        return ['id', 'module_code', 'user_id', 'content', 'record_time', 'client_ip']
        
    @classmethod
    def get_primary_key(self):
        return "id"

    def __str__(self):
        return "cms_log_action_tb"
    
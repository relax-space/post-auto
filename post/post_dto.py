
class PostDto:
    def __init__(self):
        # 职位标题
        self.title: str = ''
        # 用证地区 省
        self.province: str = ''
        # 用证地区 市
        self.city: str = ''
        # 学历要求
        self.edu: str = ''
        # 签约方式
        self.method: str = ''

        # 工作性质
        self.work_type: str = ''
        # 注册情况
        self.reg_status: str = ''
        # 职      称
        self.degree_level: str = ''
        # 证书用途
        self.cert_use: str = ''
        # 职位薪资
        self.expect_pay: str = ''

        # 职位薪资 年
        self.expect_pay_time: str = ''
        # 业绩要求
        self.yeji_needs: str = ''
        # 详细说明
        self.detail_info: str = ''
        # 分类1
        self.class1: str = ''
        # 分类2
        self.class2: str = ''

        pass

    @classmethod
    def to_dict(cls, obj):
        entry = obj.__dict__
        return entry

    @classmethod
    def from_dict(cls, dict):
        obj = PostDto()
        obj.__dict__ = dict
        return obj

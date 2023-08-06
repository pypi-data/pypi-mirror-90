import time

from optionaldict import optionaldict
from wechatpy.enterprise.client.api import WeChatExternalContact


class WeChatExternalContactChild(WeChatExternalContact):
    """
    客户联系人扩展类
    """

    def get_external_group_list(self, userid):
        """
           获取客户群列表
          https://work.weixin.qq.com/api/doc/90000/90135/92120

          status_filter: 客户群跟进状态过滤。0 - 所有列表(即不过滤),1 - 离职待继承,2 - 离职继承中,3 - 离职继承完成
          owner_filter: 群主userid过滤
                  userid_list: 企业微信员工userid列表
          cursor: 用于分页查询的游标，字符串类型，由上一次调用返回，首次调用不填
          limit: 分页，预期请求的数据量，取值范围 1 ~ 1000

        Args:
            userid:

        Returns:

        """
        cursor = ""
        group_chat_list = []
        data = optionaldict(
            status_filter=0,
            owner_filter={"userid_list": [userid]},
            cursor=cursor,
            limit=100,
        )
        try:
            while True:
                response = self._post("externalcontact/groupchat/list", data=data)
                if (response["errcode"] == 0) and response.get("cursor"):
                    cursor = response.get("cursor")
                    group_chat_list.extend(response.get("group_chat_list"))
                else:
                    break
            return group_chat_list
        except Exception as e:
            print(e)
            return []

    def get_external_group_statistic_data(
        self, userid: str, start_time: int = None, end_time: int = None
    ):
        """
            获取「群聊数据统计」数据
        Args:
            userid:
            start_time:
            end_time:

        Returns:

        """
        try:
            external_behavior_list = []
            offset = 0
            parameter = {"owner_filter": {"userid_list": [userid]}, "offset": offset}
            if start_time and end_time:
                parameter["day_begin_time"] = start_time
                parameter["day_end_time"] = end_time
            elif start_time:
                parameter["day_begin_time"] = start_time
            else:
                parameter["day_begin_time"] = time.time() - 86400
            while True:
                response = self._post(
                    "externalcontact/groupchat/statistic", data=parameter
                )
                external_behavior_list.extend(response.get("items"))
                if response.get("total") == response.get("next_offset"):
                    break
                else:
                    parameter["offset"] = response.get("next_offset")
            return external_behavior_list
        except Exception as e:
            print(e)
            return []

    def get_external_behavior_data(self, userid: str, start_time, end_time):
        """
            获取「联系客户统计」数据
        Args:
            userid:
            start_time:
            end_time:

        Returns:

        """
        try:
            if start_time and end_time:
                parameter_start_time = start_time
                parameter_end_time = end_time
            elif start_time:
                parameter_start_time = start_time
                parameter_end_time = start_time
            elif end_time:
                parameter_start_time = end_time
                parameter_end_time = end_time
            else:
                # 测试时间
                parameter_start_time = 1609224560
                parameter_end_time = 1609224560
                # parameter_start_time = time.time()
                # parameter_end_time = time.time()
            res = self.get_user_behavior_data(
                userid, parameter_start_time, parameter_end_time
            )
            if res.get("errcode") == 0:
                return res.get("behavior_data")
            else:
                return []
        except Exception as e:
            print(e)
            return []

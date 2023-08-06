# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from itertools import chain

from wechatpy.enterprise.client.api import WeChatDepartment


class WeChatDepartmentChild(WeChatDepartment):
    """
    https://work.weixin.qq.com/api/doc#90000/90135/90204
    """

    def get_map_users(self, id=None, key="name", status=0, fetch_child=0):
        """
        映射员工某详细字段到 ``user_id``

        企业微信许多对员工操作依赖于 ``user_id`` ，但没有提供直接查询员工对应 ``user_id`` 的结构，

        这里是一个变通的方法，常用于储存员工 ``user_id`` ，并用于后续查询或对单人操作（如发送指定消息）

        id: 部门 id， 如果不填，默认获取有权限的所有部门
        key: 员工详细信息字段 key，所指向的值必须唯一
        status: 0 获取全部员工，1 获取已关注成员列表，
                2 获取禁用成员列表，4 获取未关注成员列表。可叠加
        fetch_child: 1/0：是否递归获取子部门下面的成员
        dict - 部门成员指定字段到 user_id 的 map  ``{ key: user_id }``
        """
        ids = [id] if id is not None else [item["id"] for item in self.get()]
        users_info = list(
            chain(
                *[
                    self.get_users(
                        department, status=status, fetch_child=fetch_child, simple=False
                    )
                    for department in ids
                ]
            )
        )
        users_zip = [(user["userid"], user[key]) for user in users_info]
        return dict(users_zip)

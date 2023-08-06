import re
import regex

from k_parse_tool.Enum import regex_flags, item_enum

from k_parse_tool.Enum.fix_const_enum import FixConstEnum
from prettytable import basestring

from k_parse_tool.lib.column_common_reg import LawAccordingReg, AdminPenaltyDateReg, AdminPenaltyDeptReg, \
    AdminPenaltyNumberReg, AdminPenaltyPunishedPartiesReg, AdminPenaltyPunishedPeopleReg, \
    AdminPenaltyPunishedMeasuresReg


class CommonExtractData:

    @staticmethod
    def extract_data_by_common_reg(item, resource, reg_dict):

        reg_dict = CommonExtractData.add_data_to_item_by_common_reg_from_resource(reg_dict)

        CommonExtractData.extract_data_from_dict_and_resource(reg_dict, resource, item)

    @staticmethod
    def add_data_to_item_by_common_reg_from_resource(reg_dict={}):
        # 发布部门
        if item_enum.DETAIL_PAGE_DEPT not in reg_dict.keys():
            reg_dict[item_enum.DETAIL_PAGE_DEPT] = AdminPenaltyDeptReg.getCommonDeptReg()
        # 处罚日期
        if item_enum.DETAIL_PAGE_DATE not in reg_dict.keys():
            reg_dict[item_enum.DETAIL_PAGE_DATE] = AdminPenaltyDateReg.getCommonAdminPenaltyDateReg()
        # 发文字号
        if item_enum.DETAIL_PAGE_TEXT_NUMBER not in reg_dict.keys():
            reg_dict[item_enum.DETAIL_PAGE_TEXT_NUMBER] = AdminPenaltyNumberReg.getCommonNumberReg()

        # 法律依据
        if item_enum.DETAIL_PAGE_LAWACCORDING not in reg_dict.keys():
            reg_dict[item_enum.DETAIL_PAGE_LAWACCORDING] = LawAccordingReg.getCommonLawAccordingReg()
        # 处罚对象(公司)
        if item_enum.DETAIL_PAGE_PUNISHED_PARTIES not in reg_dict.keys():
            reg_dict[
                item_enum.DETAIL_PAGE_PUNISHED_PARTIES] = AdminPenaltyPunishedPartiesReg.getCommonPunishedPartiesReg()
        # 处罚负责人
        if item_enum.DETAIL_PAGE_PUNISHED_PEOPLE not in reg_dict.keys():
            reg_dict[item_enum.DETAIL_PAGE_PUNISHED_PEOPLE] = AdminPenaltyPunishedPeopleReg.getCommonPunishedPeopleReg()
        # 处罚结果
        if item_enum.DETAIL_PAGE_PUNISHMENT_MEASURES not in reg_dict.keys():
            reg_dict[
                item_enum.DETAIL_PAGE_PUNISHMENT_MEASURES] = AdminPenaltyPunishedMeasuresReg.getCommonPunishedMeasuresReg()
        return reg_dict

    @staticmethod
    # reg_dict  的key 是item的属性名称,  value  是提取该属性的正则表达式
    def extract_data_from_dict_and_resource(reg_dict, resource, item):
        if (len(reg_dict) > 0):
            for key, value in reg_dict.items():
                if key not in item.keys():
                    end_value = ""
                    # 法律依据提取多条
                    if key == item_enum.DETAIL_PAGE_LAWACCORDING:
                        list_value = regex.findall(value, resource)
                        end_value = "\r\n".join(list_value) if len(list_value) > 0 else end_value
                        end_value = CommonExtractData.get_law_according(end_value)
                    else:
                        reg_result = regex.search(value, resource)
                        if (reg_result):
                            end_value = reg_result.group()

                    item[key] = end_value

    @staticmethod
    def join_post_params_and_url(url, post_params):
        is_str = isinstance(post_params, basestring)
        join_str = ''
        if is_str:
            join_str = url + '<POST>' + post_params + '</POST>'
        else:
            str_list = []
            for key, value in post_params.items():
                str_list.append(str(key) + '=' + str(value))
            join_str = "&".join(str_list)
            join_str = url + '<POST>' + join_str + '</POST>'
        return join_str

    @staticmethod
    def get_content_by_reg(resource, reg, search_full=False, flags=regex_flags.I, timeout=10, ignore_unused=True,
                           pos=None,
                           endpos=None):
        '''
        根据正则提取文本
        :param resource:匹配时使用的文本
        :param reg:正则表达式
        :param search_full:获取所有匹配值,默认False(仅匹配第一个)
        :param flags:可选标志修饰符,默认regex_flags.I
        :param timeout:正则匹配超时时间,默认10s
        :param ignore_unused:如果有任何未使用的关键字参数,ValueError将被抛出,默认忽略错误
        :param pos:文本中正则表达式开始搜索的位置
        :param endpos:文本中正则表达式结束搜索的位置
        :return:
        '''
        result_dict = dict()
        result_dict[FixConstEnum.REG_CONTENT] = ""
        if search_full:
            list_value = regex.findall(reg, resource, flags=flags, timeout=timeout, ignore_unused=ignore_unused,
                                       pos=pos, endpos=endpos)
            result_dict[FixConstEnum.REG_CONTENT] = list_value
        else:
            reg_result = regex.search(reg, resource, flags=flags, timeout=timeout, ignore_unused=ignore_unused, pos=pos,
                                      endpos=endpos)
            if (reg_result):
                end_value = reg_result.group()
                result_dict[FixConstEnum.REG_CONTENT] = end_value
        return result_dict

    @staticmethod
    def get_law_according(resource):
        law_reg = LawAccordingReg.getCommonLawAccordingReg()
        list_value = regex.findall(law_reg, resource)
        end_value = "\r\n".join(list_value) if len(list_value) > 0 else ''
        return end_value

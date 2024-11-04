# coding: utf-8

tm_map = {"考试时间":4, "网上缴费":2, "打印准考证":2, "提交报考申请":2}
def set_tm(patterns, v):
    for k in patterns:
        tm_map[k] = tm_map[v]
    
baoming_pattern = ["报名方式、时间", "报名时间是", "提交报名申请" , "提交报考申请", "提交申请",  "报名时间" , "网上报名"]
set_tm(baoming_pattern, "提交报考申请")
# 提取模式： url  在最近三行以内执行该逻辑
# b = "查询资格审查结果",  "资格初审",  "查询初审结果"  获取之后几行时间
 
kaoshi_time_pattern1 = ["公共科目考试时间", "考试内容和时间", "笔试面试", "笔试计划", "笔试时间" , "考试科目", "笔试"]
set_tm(kaoshi_time_pattern1, "考试时间")


kaoshi_time_pattern2 = ["专业科目考试时间",  "公共科目考试时间", "公共科目笔试时间"]
set_tm(kaoshi_time_pattern2, "考试时间")


fee_time_pattern = ["报名确认及网上缴费", "报名及网上缴费", "网上缴费", "缴费确认","网络缴费", "打印.*?准考证"]
set_tm(fee_time_pattern, "网上缴费")


access_time_pattern = ["打印准考证", "打印",  "准考证打印"]  #  正则匹配的方式获取 取其中一行
set_tm(access_time_pattern, "打印准考证")

ex_pattern = [baoming_pattern, kaoshi_time_pattern1, kaoshi_time_pattern2, fee_time_pattern, access_time_pattern]

fj = "附件"   # startswith 往下遍历 6行，且带有href 属性 
tm_map[fj] = 6
# 来源:  可以试试 optional
# 于.*?发布

key_pat = {}
key_pat["报名"] = baoming_pattern
key_pat["考试"] = kaoshi_time_pattern1
key_pat["缴费"] = fee_time_pattern
key_pat["准考证"] = access_time_pattern
key_pat["all"] = access_time_pattern

# zwk_zwlx 考试类型 
zwlx_list = ["公务员","国家公务员","省公务员","选调生","定向招录","公安招警","军队文职","军转干",
        "退役士兵","事业编","人才引进","教师编","特岗教师","医院招聘","规范培训",
        "公开遴选","公开选调","公开选拔","央企","国企","银行","人民银行","农信社",
        "大学生村官","三支一扶","基层工作者","社区工作者","公益岗位","辅警"]


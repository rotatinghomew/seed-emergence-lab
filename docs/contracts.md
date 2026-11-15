# 资料与接口约定

## 领域记录
climate 行按 house-day 记温度和停机；inspection 行的 new_emerged 是 (last_day,day] 内新增可见出苗数，不是累计数。disease_removed 为尚未出苗穴中退出数；destructive_removed 为整盘取走的当时未出苗穴，取走后不再巡查。已出苗、病害和抽盘三者互斥。初始盘穴数在 houses.cells_per_tray。POST /quote 传 house、start_day、end_day，返回左闭右开区间积温及缺失天，offline 不产生有效积温观测；POST /detail 传 house 返回盘容量和订单截止日。order_deadlines 的 plants 是可移栽苗数，不是投种穴数。

各温室 houses.post_emergence_days 是固定养护天数，出苗满此天数即可计为可移栽；该批合成记录中没有出苗后死亡、出苗前缺穴或额外长势分级。对区间出苗应传播其对就绪时刻的不确定性。POST /detail 同时返回此规则，不能把出苗当日立即计为交苗就绪。

## 冻结来源
GET /manifest 返回 release、digest、row_count、metadata。digest 对完整领域资料按 JSON 键排序、紧凑分隔和 UTF-8 计算 SHA-256。
GET /records 及后续 cursor 请求、POST /quote、POST /detail 都要求 If-Match 等于清单 release，否则返回 412。
游标仅用于所属版本，客户端不能自行猜测页数。source 进程在启动时固定加载 data/release.json。
业务请求成功返回 release、request、result；业务值非法返回 422，游标不合法返回 400，未知地址返回 404。
仅有资料概览与领域核价，不含方案选型、统计推断或预测能力。

## 已有消费接口
GET /health 返回 status=ok；GET /overview 返回 release、digest 与描述性 overview。
POST /quotes 的 JSON 为 release 和 request，结果转发来源方回执。
POST /reports 接受 release、source_digest、kind、result、receipts，返回内容寻址 id；相同内容重复保存得到同一 id。
GET /reports/{id} 返回 id 与原 payload，重启后仍可读，不重算来源资料；不存在时 404。
这些接口的字段和返回类型保持兼容，新增业务可以扩展而不改变旧档案内容。
数据数值保留原始精度；只有领域服务中已标注的金额按对应货币规则处理。

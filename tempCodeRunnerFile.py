import traceback
import random
from tqdm import trange
import json
import argparse

# 中文泛化模板
question_templates_zh = [
    "玛格丽特继承了[输入槽位1]美元，她打算将这笔钱投入年平均回报率[输入槽位2]的低成本指数基金，10年内不再追加任何投资（全程月复利）。十年后她计划将前10年的本金和利息作为现在的本金，并在接下来20年每月追加[输入槽位3]美元本金（月末追加）。这20年也结束后，期末本金是多少？将这个期末本金作为现在的本金之后，该基金每月能得到多少利息用于生活？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程用同一高精度浮点，至少双精度 64 位，不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数，在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "莉莲娜获得了[输入槽位1]美元的科技竞赛一等奖奖金，她打算将这笔钱投入年平均回报率[输入槽位2]的低成本被动型指数基金，10年内不再追加任何投资（全程按每月复利计算收益）。十年后，她计划把前10年积累的本金与利息总和作为新的投资本金，并在接下来20年里每月月末追加[输入槽位3]美元。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能产生多少利息用于日常生活？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程使用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "詹姆斯收到了已故叔叔留下的[输入槽位1]美元遗赠，他打算将这笔钱投入年平均回报率[输入槽位2]的低成本ETF基金，头10年不追加任何投资（全程采用月复利计算）。十年期满后，他会把前10年的本金与利息总和作为新的投资本金，并在接下来的20年里每月月末追加[输入槽位3]美元本金。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能产生多少利息用于退休生活开支？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "艾丽西亚继承了母亲遗留的[输入槽位1]美元存款，她打算将这笔钱投入年平均回报率[输入槽位2]的低成本指数基金，10年内不再追加任何投资（全程按每月复利计算）。十年后，她以这10年的本金与利息总和作为新的初始本金，并在接下来20年里每月月末额外投入[输入槽位3]美元。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能提供多少利息用于覆盖生活成本？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "托马斯中了[输入槽位1]美元的州彩票二等奖，他将这笔钱投入年平均回报率[输入槽位2]的低成本指数型ETF，10年内不再追加任何投资（全程按每月复利计算收益）。十年后，他把这10年的本金与利息总和作为新的投资本金，并在接下来20年里每月月末补充投入[输入槽位3]美元。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能产生多少利息用于支付日常开销？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "伊莎贝尔出售家族老房子获得了[输入槽位1]美元，她打算将这笔钱投入年平均回报率[输入槽位2]的低成本指数基金，10年内不追加任何资金，全程以每月复利计算收益。十年后，她将前10年积累的本利和作为新的本金，并在接下来20年里每月月末追加[输入槽位3]美元本金。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能带来多少利息用于生活开支？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程使用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "张明获得了[输入槽位1]美元的工作奖金，他打算将这笔钱投入年平均回报率[输入槽位2]的低成本指数基金，10年内不再追加任何投资（全程按每月复利计算收益）。十年后，他计划把前10年积累的本金与利息总和作为新的投资本金，并在接下来20年里每月月末追加[输入槽位3]美元。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能产生多少利息用于日常生活？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程使用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）",
    "李华继承了[输入槽位1]美元的家族遗产，他打算将这笔钱投入年平均回报率[输入槽位2]的低成本指数基金，10年内不再追加任何投资（全程按每月复利计算收益）。十年后，他计划把前10年积累的本金与利息总和作为新的投资本金，并在接下来20年里每月月末追加[输入槽位3]美元。这20年结束后，期末本金是多少？将这个期末本金作为当前本金之后，该基金每月能产生多少利息用于日常生活？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程使用同一高精度浮点（至少双精度64位），不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数。在计算出保留两位小数的期末本金和30年后的每月利息后，由于需消除部分浮点精度误差，要分别取这两者的整数部分（不用四舍五入，且期末本金的整数部分的个位上的数字需要被置为1）作为该问题的最终答案）"
]

# 英文泛化模板
question_templates_en = [
    "Margaret inherited [输入槽位1] dollars. She plans to invest this amount into a low-cost index fund with an annual average return rate of [输入槽位2], making no additional contributions for 10 years (compounded monthly throughout). Ten years later, she intends to use the principal plus interest accumulated from the first 10 years as the new principal, and then contribute [输入槽位3] dollars each month (added at the end of each month) for the following 20 years. After these 20 years conclude, what is the final account balance? Using this final balance as the current principal, how much monthly interest can the fund generate for living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "David, a software engineer at a tech startup, received a $[输入槽位1] performance bonus. He aims to save this for early retirement by first investing it in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without any additional contributions. After a decade, he plans to use the accumulated principal plus interest as the new base and add [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years are over, what is the final account balance? Using this balance as the current principal, how much monthly interest can the fund generate to cover his living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Emily, a lifelong librarian planning for retirement, received a $[输入槽位1] gift from her late grandmother. She intends to grow this money by investing it in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years with no extra deposits. After those 10 years, she'll use the total principal plus interest as the new principal and contribute [输入槽位3] dollars each month (added at the end of each month) for the following 20 years. Once these 20 years conclude, what is the final account balance? Using this final balance as the current principal, how much monthly interest can the fund generate for her living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Carlos, a construction worker who received a $[输入槽位1] legal settlement, wants to secure his family's future by investing this amount. First, he'll put the money into a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without additional contributions. After a decade, he'll take the accumulated principal plus interest as the new principal and add [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years end, what is the final account balance? Using this final balance as the current principal, how much monthly interest can the fund generate for his family's living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Lila, an artist who sold her downtown art studio for $[输入槽位1], plans to retire early by growing this funds. She'll first invest the entire amount in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years with no extra contributions. After 10 years, she'll use the accumulated principal plus interest as the new principal and contribute [输入槽位3] dollars each month (added at the end of each month) for the following 20 years. After these 20 years conclude, what is the final account balance? Using this final balance as the current principal, how much monthly interest can the fund generate for her living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Mr. Thompson, a retired high school teacher, inherited $[输入槽位1] from his late uncle. To supplement his retirement income, he plans to first invest this amount in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without additional contributions. After a decade, he'll use the accumulated principal plus interest as the new principal and contribute [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years conclude, what is the final account balance? Using this final balance as the current principal, how much monthly interest can the fund generate for his living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Sarah, a teacher saving for her children's education, received a $[输入槽位1] inheritance from her aunt. She plans to invest this in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without any additional contributions. After 10 years, she'll use the accumulated principal plus interest as the new base and add [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years are over, what is the final account balance? Using this balance as the current principal, how much monthly interest can the fund generate to cover her children's educational expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Michael, a nurse planning for early retirement, received a $[输入槽位1] bonus from his hospital. He decides to invest this in a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without any additional contributions. After a decade, he plans to use the accumulated principal plus interest as the new base and add [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years are over, what is the final account balance? Using this balance as the current principal, how much monthly interest can the fund generate to cover his living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)",
    "Lisa, a marketing manager, received a $[输入槽位1] commission bonus. She wants to invest this for her future by first putting it into a low-cost index fund with an annual average return rate of [输入槽位2], compounded monthly, for 10 years without any additional contributions. After 10 years, she'll use the accumulated principal plus interest as the new base and add [输入槽位3] dollars each month (at the end of every month) for the next 20 years. When these 20 years are over, what is the final account balance? Using this balance as the current principal, how much monthly interest can the fund generate to cover her living expenses?\n\n(The calculation must strictly adhere to the values specified in the problem; the computational process must be rigorous and valid, and the results must be correct and reproducible. The entire computation must use the same high-precision floating-point format—no less than IEEE 754 double precision (64-bit)—with no rounding at any intermediate step to ensure no loss of precision. Only at the very end, when reporting the final balance after 30 years and the corresponding monthly interest, should both values be rounded to two decimal places. After obtaining these two values rounded to two decimal places, and in order to mitigate minor floating-point precision artifacts, take the integer part of each (without rounding). Additionally, the units digit (the ones place) of the integer part of the final balance must be set to 1. These two resulting integers constitute the final answer to the problem.)"
]

def input(difficulty, language): 

    # 题目基础参数，包括难度，随机数种子
    params = {
        "difficulty": difficulty,
        "seed": random.randint(1, 10_000),
    } 
    
    # 难度映射，用于存储不同难度下题目难度相关数据的各项参数
    # 格式：(初始金额范围, 年回报率范围, 每月追加金额范围)
    diff_map = {
        1: ((1000), (0.012), (1)), 
        2: ((4000), (0.012), (2)), 
        3: ((7000), (0.012), (4)),  
        4: ((1000), (0.024), (8)), 
        5: ((3000), (0.024), (8)), 
        6: ((6000), (0.024), (8)), 
        7: ((8000, 15000), (0.008, 0.012), (40)),
        8: ((15000, 30000), (0.012, 0.016), (1500, 2000)),
        9: ((30000, 60000), (0.016, 0.02), (2000, 3000)),
        10: ((60000, 100000), (0.02, 0.04), (3000, 5000))
    }    

    
    # 获取当前难度的参数范围
    initial_range, rate_range, monthly_add_range = diff_map[difficulty]
    
    # 生成随机参数
    # 处理初始金额
    if isinstance(initial_range, tuple) and len(initial_range) == 2:
        initial_amount = random.randint(initial_range[0], initial_range[1])
    else:
        initial_amount = initial_range
    
    # 处理年回报率
    if isinstance(rate_range, tuple) and len(rate_range) == 2:
        annual_rate = round(random.uniform(rate_range[0], rate_range[1]), 4)
    else:
        annual_rate = rate_range
    
    # 处理每月追加金额
    if isinstance(monthly_add_range, tuple) and len(monthly_add_range) == 2:
        monthly_add = random.randint(monthly_add_range[0], monthly_add_range[1])
    else:
        monthly_add = monthly_add_range
    
    
    # 更新参数
    params.update({
        "initial_amount": initial_amount,
        "annual_rate": annual_rate,
        "monthly_add": monthly_add
    })
    
    # 生成槽位文本
    slot_texts = [
        str(initial_amount),
        str(annual_rate),
        str(monthly_add)
    ]
    
    return params, slot_texts

def solution(params, language):

    # 提取参数
    initial_amount = params["initial_amount"]
    annual_rate = params["annual_rate"]
    monthly_add = params["monthly_add"]
    
    # 计算月利率
    monthly_rate = annual_rate / 12
    
    # 计算前10年的期末金额（月复利）
    # FV = P * (1 + r)^n
    years_1 = 10
    months_1 = years_1 * 12
    fv1 = initial_amount * (1 + monthly_rate) ** months_1
    
    # 计算接下来20年的期末金额（月复利 + 每月追加）
    # FV = PV * (1 + r)^n + PMT * [((1 + r)^n - 1) / r]
    years_2 = 20
    months_2 = years_2 * 12
    fv2 = fv1 * (1 + monthly_rate) ** months_2 + monthly_add * (((1 + monthly_rate) ** months_2 - 1) / monthly_rate)
    
    # 计算每月利息
    monthly_interest = fv2 * monthly_rate
    
    # 保留两位小数
    fv2_rounded = round(fv2, 2)
    monthly_interest_rounded = round(monthly_interest, 2)
    
    # 取整数部分（不用四舍五入）
    # 期末本金：将个位置为1
    fv2_integer = (int(fv2_rounded) // 10 * 10) + 1
    # 每月利息：保留个位
    monthly_interest_integer = int(monthly_interest_rounded)
    
    # 生成答案
    if language == "zh":
        answer = f"期末本金：{fv2_integer} 美元，每月利息：{monthly_interest_integer} 美元"
    else:
        answer = f"Final principal: {fv2_integer} dollars, Monthly interest: {monthly_interest_integer} dollars"

    return answer

# 题目模板，用于生成题目随机选择。
def QUESTIYPE_GEN(difficulty, language="en"):
    question_templates = question_templates_en if language == "en" else question_templates_zh
    question_template = random.choice(question_templates)
    input_params, input_slot_texts = input(
        difficulty=difficulty,
        language=language,
    )
    answer = solution(input_params, language=language) # 首先生成题目，然后再生成答案

    # 槽位占位符用于统一替换，保持不变以兼容既有数据。
    now_question = question_template
    slot_idx = 1
    for slot_text in input_slot_texts:
        now_question = now_question.replace(f"[输入槽位{slot_idx}]", str(slot_text))
        slot_idx += 1
        
    return now_question, answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group()
    # 单个脚本运行参数，必填参数有3个，分别是样本数量，难度范围，语言。难度范围格式参照需求文档，要求支持3种格式。
    group.add_argument(
        "--sample-time",
        type=int,
        help="每个难度生成的样本数量。",
    )
    group.add_argument(
        "--difficulty",
        type=str,
        help="难度范围",
    )
    group.add_argument(
        "--language",
        type=str,
        default="zh",
        help="语言，如 'en' 或 'zh'。",
    )
    group.add_argument(
        "--output-path", 
        type=str, 
        default="./investment_calculation.jsonl",
        help="输出路径",
    )
    
    # 全量参数${python script.py --sample-time 100 --difficulty [2,5,8] --language en --output-path ./output.jsonl}
    
    args = parser.parse_args()
    
    # 交互式输入模式
    if not args.sample_time or not args.difficulty:
        import sys
        print("===== 交互式输入模式 =====")
        # 输入采样量
        while True:
            try:
                print("请输入采样量（每个难度生成的样本数量）: ", end="")
                sample_time = int(sys.stdin.readline().strip())
                if sample_time > 0:
                    args.sample_time = sample_time
                    break
                else:
                    print("采样量必须大于0，请重新输入")
            except ValueError:
                print("请输入有效的整数")
        
        # 输入难度
        while True:
            print("请输入难度（支持整数、列表[2,5,7]或范围[3-10]）: ", end="")
            difficulty_input = sys.stdin.readline().strip()
            args.difficulty = difficulty_input
            try:
                # 验证难度格式
                difficulty_str = args.difficulty
                difficulty_list = []
                
                if difficulty_str.startswith("[") and difficulty_str.endswith("]"):
                    inner_str = difficulty_str[1:-1]
                    if "-" in inner_str:
                        diff_start, diff_end = map(int, inner_str.split("-"))
                        if diff_start > diff_end:
                            raise ValueError("起始难度不能大于结束难度")
                        difficulty_list = list(range(diff_start, diff_end + 1))
                    else:
                        difficulty_list = json.loads(difficulty_str)
                        if not isinstance(difficulty_list, list):
                            raise ValueError("列表格式不正确")
                elif "-" in difficulty_str:
                    diff_start, diff_end = map(int, difficulty_str.split("-"))
                    if diff_start > diff_end:
                        raise ValueError("起始难度不能大于结束难度")
                    difficulty_list = list(range(diff_start, diff_end + 1))
                else:
                    difficulty_list = [int(difficulty_str)]
                
                for diff in difficulty_list:
                    if diff < 1 or diff > 10:
                        raise ValueError(f"难度必须在1-10之间，当前值：{diff}")
                
                if not difficulty_list:
                    raise ValueError("难度范围为空")
                break
            except Exception as e:
                print(f"难度格式错误：{e}，请重新输入")
        
        # 输入语言
        print("请输入语言（zh-中文，en-英文，默认zh）: ", end="")
        language_input = sys.stdin.readline().strip()
        if language_input in ["zh", "en"]:
            args.language = language_input
        
        # 输入输出路径
        print("请输入输出路径（默认./investment_calculation.jsonl）: ", end="")
        output_path_input = sys.stdin.readline().strip()
        if output_path_input:
            args.output_path = output_path_input
        
        print("=========================")

    # 解析难度参数，支持三种格式：整数、列表、范围
    try:
        difficulty_list = []
        difficulty_str = args.difficulty
        
        # 处理带方括号的情况
        if difficulty_str.startswith("[") and difficulty_str.endswith("]"):
            # 去掉方括号
            inner_str = difficulty_str[1:-1]
            # 检查是范围还是列表
            if "-" in inner_str:
                # 带方括号的范围格式，如 "[2-8]"
                diff_start, diff_end = map(int, inner_str.split("-"))
                if diff_start > diff_end:
                    raise ValueError("起始难度不能大于结束难度")
                difficulty_list = list(range(diff_start, diff_end + 1))
            else:
                # 列表格式，如 "[2,5,7]"
                difficulty_list = json.loads(difficulty_str)
                if not isinstance(difficulty_list, list):
                    raise ValueError("列表格式不正确")
        elif "-" in difficulty_str:
            # 不带方括号的范围格式，如 "3-10"
            diff_start, diff_end = map(int, difficulty_str.split("-"))
            if diff_start > diff_end:
                raise ValueError("起始难度不能大于结束难度")
            difficulty_list = list(range(diff_start, diff_end + 1))
        else:
            # 单个整数，如 "3"
            difficulty_list = [int(difficulty_str)]
        
        # 验证难度范围
        for diff in difficulty_list:
            if diff < 1 or diff > 10:
                raise ValueError(f"难度必须在1-10之间，当前值：{diff}")
        
        if not difficulty_list:
            raise ValueError("难度范围为空")
    except Exception as e:
        raise RuntimeError(
            "解析 --difficulty 失败，期望格式如 '3'、'[2,5,7]' 或 '[2-8]'：%s" % e
        )

    per_difficulty_count = args.sample_time
    difficulty_len = len(difficulty_list)
    total = difficulty_len * per_difficulty_count

    with open(args.output_path, "w", encoding="utf-8") as f_write, \
        trange(total, desc="generating") as pbar:
        for diff in difficulty_list:
            for _ in range(per_difficulty_count):
                retry = 10
                success = False
                while retry > 0:
                    try:
                        question, answer = QUESTIYPE_GEN(difficulty=diff, language=args.language) # 生成题目需要两个参数，分别是难度和语言   
                        # 单个题目json的字段,包含6个字段
                        record = {
                            "question": question,
                            "answer": str(answer),
                            "task": "逻辑推理/合成/数字操作/指令按步骤执行-计算复杂/投资计算",
                            "tag": "数字操作/指令按步骤执行/计算复杂",
                            "difficulty": diff,
                            "task_id": "investment_calculation",
                        }
                        f_write.write(json.dumps(record, ensure_ascii=False) + "\n")
                        success = True
                        break
                    except Exception:
                        traceback.print_exc()
                        retry -= 1
                if not success:
                    raise RuntimeError(
                        "难度 %s 生成失败，重试 10 次仍未成功" % diff
                    )
                pbar.update(1)

    print(
        "完成：生成 %s 条样本（%s 个难度 x 每个 %s 条），已保存到 %s"
        % (total, difficulty_len, per_difficulty_count, args.output_path)
    )


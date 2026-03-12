import json

# 导入交付py框架中的函数
from 交付py框架 import solution

# 模拟完整流程
def test_complete_flow():
    """
    模拟交付py框架.py的完整流程，输出指定问题的json格式结果
    """
    # 创建与问题完全匹配的参数
    test_params = {
        "initial_amount": 10000,  # 初始金额：1万美元
        "annual_rate": 0.08,      # 年回报率：8%
        "monthly_add": 200        # 每月追加：200美元
    }
    
    # 调用solution函数计算答案
    answer = solution(test_params, "zh")
    
    # 生成题目文本
    question = "玛格丽特继承了10000美元，她打算将这笔钱投入年平均回报率0.08的低成本指数基金，10年内不再追加任何投资（全程月复利）。十年后她计划将前10年的本金和利息作为现在的本金，并在接下来20年每月追加200美元本金（月末追加）。这20年也结束后，期末本金是多少？将这个期末本金作为现在的本金之后，该基金每月能得到多少利息用于生活？（计算所用数字必须严格按照题目要求，计算过程必须严谨合法，计算结果必须正确可复现，全程用同一高精度浮点，至少双精度 64 位，不中途四舍五入，务必不要丢失精度，只在最后计算期末本金以及30年后的每月利息上保留两位小数，在计算出保留两位小数的期末本金和30年后的每月利息后，分别取这两者的整数部分（不用四舍五入）作为该问题的最终答案）"
    
    # 生成json记录
    record = {
        "question": question,
        "answer": answer,
        "task": "逻辑推理/合成/数字操作/指令按步骤执行-计算复杂/投资计算",
        "tag": "数字操作/指令按步骤执行/计算复杂",
        "difficulty": 5,
        "task_id": "investment_calculation"
    }
    
    # 输出json格式
    json_output = json.dumps(record, ensure_ascii=False)
    print(json_output)
    
    # 同时保存到文件
    with open("./specific_question_output.jsonl", "w", encoding="utf-8") as f:
        f.write(json_output + "\n")
    print("\n已保存到 specific_question_output.jsonl 文件")

if __name__ == "__main__":
    test_complete_flow()

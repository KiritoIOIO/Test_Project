import traceback
from tqdm import trange
import numpy as np
import random

# 这里只有一个中文模板，请根据标注要求自行扩充，本部分内容一定与平台中相关字段保持一致
question_templates_zh = [
    "这是一道逻辑题，请按如下规则完成：\n"
    "1）仔细阅读题干。\n"
    "2）根据示例推导方法。\n\n"
    "[示例]\n"
    "[输入槽位1] -> [输入槽位2]\n\n"
    "现在开始作答：\n"
    "[输入槽位3]",
    "在一次训练中，学生收到一道任务。\n"
    "规则已在题干中给出。\n\n"
    "示例： [输入槽位1]\n\n"
    "输入： [输入槽位2]\n"
    "问题： [输入槽位3]",
]

# 请根据标注要求自行扩充，本部分内容一定与平台中相关字段保持一致
question_templates_en = [
    "This is a logic problem. Please follow the rules below:\n"
    "1) Read the problem carefully.\n"
    "2) Derive the method from the example.\n\n"
    "[Example]\n"
    "[Input Slot 1] -> [Input Slot 2]\n\n"
    "Now start answering:\n"
    "[Input Slot 3]",
    "In a training session, students receive a task.\n"
    "Rules are given in the problem statement.\n\n"
    "Example: [Input Slot 1]\n\n"
    "Input: [Input Slot 2]\n"
    "Question: [Input Slot 3]",
]

def input(difficulty, language): #对应原def_input文件:
    """
    生成 solution() 所需参数以及题干模板的填充槽位文本。
    **重要**：slot_texts_list 中的文本必须与 question_templates 中的占位符一一对应，否则会导致生成的题目无法正常显示。
    **重要**： 平台验证代码可用时，会调用该函数 
    返回：(params_for_solution, slot_texts_list)
    """
    
    # 由于平台在校验代码块时，部分内置模块没有导入，所以在平台校验中需要手动导入部分模块。交付的py文件请将该部分删除，并按照python规范将导入模块放在文件开头
    
    """
    import random
    import re
    """
    
    # 下面的内容全部替换为具体任务的生成逻辑，以下部分参数仅供参考
    #题目基础参数，包括难度，随机数种子
    params = {
        "difficulty": difficulty,
        "seed": random.randint(1, 10_000),
    } 
    
    # 难度映射，用于存储不同难度下题目难度相关数据的各项参数。根据题目实际情况进行设置即可
    diff_map = {
        1: 3, 2: 4, 3: 9, 4: 10, 5: 12,
        6: 15, 7: 24, 8: 26, 9: 30, 10: 49
    }

    
    slot_texts = [
        "槽位文本1",
        "槽位文本2",
        "槽位文本3",
    ]
    return params, slot_texts

def solution(params, language):
    """
    基于 generate_input_params() 生成的参数求解。
    **重要**： 平台验证代码可用时，会调用该函数。
    """
    
    # 由于平台在校验代码块时，部分内置模块没有导入，所以在平台校验中需要手动导入部分模块。交付的py文件请将该部分删除，并按照python规范将导入模块放在文件开头
    
    """
    import random
    import re
    """
    
    # 替换为具体任务的解题逻辑。
    answer = "答案" 

    return answer

# 题目模板，用于生成题目随机选择。一道种子题需要扩写多个模板用于随机选择。需要准备中文模板和英文模板
# 平台不一定能够正常识别中英文模板，如果发生情况及时联系

def QUESTIYPE_GEN(difficulty, language="en"):
    question_templates = question_templates_en if language == "en" else question_templates_zh
    question_template = random.choice(question_templates)
    input_params, input_slot_texts = input(
        difficulty=difficulty,
        language=language,
    )
    answer = solution(input_params, language=language) # 首先生成题目，然后再生成答案

    # 槽位占位符用于统一替换，保持不变以兼容既有数据。
    slot_idx = 1
    now_question = question_template
    for slot_text in input_slot_texts:
        now_question = now_question.replace(
            "[输入槽位%d]" % slot_idx, str(slot_text)
        )
        slot_idx += 1
        
    return now_question, answer


if __name__ == "__main__":
    """
    程序入口，用于生成题目。
    """
    import json
    import argparse

    parser = argparse.ArgumentParser()
    group = parser.add_argument_group()
    # 单个脚本运行参数，必填参数有3个，分别是样本数量，难度范围，语言。难度范围格式参照需求文档，要求支持3种格式。
    group.add_argument(
        "--sample-time",
        type=int,
        required=True,
        help="每个难度生成的样本数量。",
    )
    group.add_argument(
        "--difficulty",
        type=str,
        required=True,
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
        default="./output.jsonl",
        help="输出路径",
    )
    
    # 最后批量运行的时候，会以${python script.py --sample-time 100 --difficulty [2,5,8]}命令行调用。单个脚本运行时间不要太长
    # 全量参数${python script.py --sample-time 100 --difficulty [2,5,8] --language en --output-path ./output.jsonl}
    
    group.add_argument("--output-path", type=str, default="./output.jsonl")
    args = parser.parse_args()

    try:
        diff_start, diff_end = map(int, args.difficulty.split("-"))
        if diff_start > diff_end:
            raise ValueError("起始难度不能大于结束难度")
        # TODO: 这里需要修改，以支持3种难度范围的可能输入
        difficulty_list = list(range(diff_start, diff_end + 1))
        if not difficulty_list:
            raise ValueError("难度范围为空")
    except Exception as e:
        raise RuntimeError(
            "解析 --difficulty 失败，期望格式如 '3-8'：%s" % e
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
                            'task': "逻辑推理/合成/{$题型}/{$考点}-{$难点}/找嫌犯",# 要求任务名为中文且唯一 ，例如：逻辑推理/合成/objcet操作/现实场景应用题/{$考点}-{$难点}/找嫌犯
                            "tag": "{$题型}/{$考点}/{$难点}",
                            "difficulty": diff,
                            "task_id": "task_id_placeholder",
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


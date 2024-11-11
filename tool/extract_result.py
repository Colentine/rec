import re

from langchain_core.messages import AIMessage


#example = '( [题目2] > [题目1] > [题目4] > [题目9] > [题目8] > [题目12] > [题目13] > [题目6] > [题目15] > [题目16] > [题目17] > [题目19] > [题目18] > [题目7] > [题目20] > [题目5] > [题目14] > [题目10] > [题目11] > [题目3] )\n\n解释'


def extract_result(message:AIMessage):
    if isinstance(message, AIMessage):
        text = message.content
    else:
        text = message

    #pattern1 = "\((.*?)\)"
    pattern2 = "\[题目(\d{1,2})\]"
    #res = re.findall(pattern1, text)
    final_res = re.findall(pattern2, text)
    return list(map(str,final_res))


#print(extract_result(example))


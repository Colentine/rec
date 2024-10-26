import argparse
import json

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from tqdm import tqdm

from tool.extract_result import extract_result

parser = argparse.ArgumentParser()
parser.add_argument("--model_name", "-m", type=str, help="输入模型名字，例如gpt-4o,gpt-3.5-turbo", required=True)
parser.add_argument("--api_key", "-a", type=str, help="输入api key", required=True)
parser.add_argument("--base_url", "-b", type=str, help="输入base url", required=True)
args = parser.parse_args()

def create_model(model_name: str, api_key: str, base_url: str):
    return ChatOpenAI(model=model_name, temperature=0.9,
                      api_key=api_key, base_url=base_url)

def create_prompt_template():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", "You are a helpful assistant.",
            ),
            ("human",
             "{query}\n\n" + "给定20道习题及用户查询和习题考察的知识点，请根据习题与查询的相关性从高到低排序，并按以下格式输出结果：( [题目1] > [题目2] > … > [题目20] )。确保格式与例示完全一致，所有20个题目均在()内且用 '>' 分隔。"
             ),
        ]
    )
    return prompt


def main():
    # 创建模型
    test_llm = create_model(model_name=args.model_name, base_url=args.base_url, api_key=args.api_key)

    # 创建Prompt
    input_prompt = create_prompt_template()

    chain = input_prompt | test_llm


    with open("data/prompt_list.json", "r", encoding="utf-8") as f:
        prompt_list = json.load(f)
        labels = prompt_list["labels"]
        top_5 = 0
        top_3 = 0
        top_1 = 0
        out_put_error = 0
        acc_pos = 0
        for idx, prompt in tqdm(enumerate(prompt_list['prompts'][0:100])):

            #print(chain.invoke({"query": prompt}))
            res = chain.invoke({"query": prompt})
            try:
                res = extract_result(res)
                pos = res.index(str(labels[idx] + 1))
            except Exception as e:
                out_put_error += 1
                pos = 20
            # print(res, labels[idx] + 1)
            if pos + 1 <= 5:
                top_5 += 1
            if pos + 1 <= 3:
                top_3 += 1
            if pos + 1 <= 1:
                top_1 += 1
            acc_pos += pos
            #print(pos, top_5, top_3, top_1, out_put_error, acc_pos)


    list_result = \
        {
            'hit5': top_5 / 100,
            'hit3': top_3 / 100,
            'hit1': top_1 / 100,
            'error_rate': out_put_error / 100,
            'avg_pos': acc_pos / 100
        }

    with open("result.json", "r", encoding="utf-8") as f:
        res = json.load(f)

    res[args.model_name] = list_result

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # print(config.YTDLP_COMMAND)
    main()

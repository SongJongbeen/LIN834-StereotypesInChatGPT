from openai import OpenAI
from dotenv import load_dotenv
import os
import yaml
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))

def load_prompt_template():
    # YAML 파일에서 프롬프트 템플릿 로드
    with open("data/base_prompts.yaml", "r", encoding="utf-8") as f:
        prompt_template = yaml.safe_load(f)
    return prompt_template

def get_categories():
    # read json
    with open("data/categories.json", "r", encoding="utf-8") as f:
        categories = json.load(f)
    return categories

categories = get_categories()
politicals = categories["political"]

def ask():
    for category in categories:
        # 디렉토리가 없는 경우 생성
        os.makedirs(f"outputs/{category}", exist_ok=True)

        for value in categories[category]:
            print(f"processing {category}/{value}")
            prompt = load_prompt_template()
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": prompt["system"]["content"]
                    },
                    {
                        "role": "user",
                        "content": prompt["user"]["content"].format(value=value)
                    }
                ],
                temperature=0.0,
                max_tokens=300,
                top_p=1.0,
                response_format={"type": "json_object"}
            )

            with open(f"outputs/{category}/{value}.json", "w", encoding="utf-8") as f:
                json.dump(json.loads(response.choices[0].message.content), f, ensure_ascii=False, indent=2)

            print(f"saved {category}/{value}.json")
        break

ask()

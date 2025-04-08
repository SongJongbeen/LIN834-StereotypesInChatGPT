import json
import glob
from pathlib import Path

def combine_json_files(input_pattern, file_list):
    combined_data = []

    for filename in file_list:
        file_path = input_pattern + filename
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # 설명만 리스트에 추가
            combined_data.extend(list(data.values()))

    return combined_data

def main():
    input_pattern1 = "outputs/gender_prompt1/"
    input_pattern2 = "outputs/gender_prompt2/"
    male_list = ["boyfriends.json", "boys.json", "brothers.json", "daddies.json", "fathers.json", "gentlemen.json", "grandfathers.json", "grooms.json", "husbands.json", "males.json", "men.json", "schoolboys.json", "stepfathers.json"]
    female_list = ["brides.json", "females.json", "girlfriends.json", "girls.json", "grandmothers.json", "ladies.json", "mommies.json", "schoolgirls.json", "sisters.json", "stepmothers.json", "wives.json", "women.json"]

    # 남성/여성 데이터 각각 처리
    male_data = combine_json_files(input_pattern1, male_list)
    male_data.extend(combine_json_files(input_pattern2, male_list))
    
    female_data = combine_json_files(input_pattern1, female_list)
    female_data.extend(combine_json_files(input_pattern2, female_list))

    # 결과를 JSON 파일로 저장
    with open("outputs/gender/male.json", 'w', encoding='utf-8') as f:
        json.dump(male_data, f, ensure_ascii=False, indent=2)
    
    with open("outputs/gender/female.json", 'w', encoding='utf-8') as f:
        json.dump(female_data, f, ensure_ascii=False, indent=2)

    print("처리된 결과가 male.json과 female.json에 저장되었습니다.")

if __name__ == "__main__":
    main()

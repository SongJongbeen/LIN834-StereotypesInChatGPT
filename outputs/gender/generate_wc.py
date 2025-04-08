import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import requests

def download_nrc_lexicon():
    """NRC 감정 사전 다운로드"""
    url = "https://raw.githubusercontent.com/beefoo/text-analysis/master/lexicons_external/NRC-Emotion-Lexicon-v0.92/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
    response = requests.get(url)
    
    lexicon = {}
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if line.strip():  # 빈 줄 제외
                try:
                    word, emotion, value = line.strip().split('\t')
                    word = word.lower()  # 단어를 소문자로 변환
                    if word not in lexicon:
                        lexicon[word] = set()
                    if value == '1':
                        lexicon[word].add(emotion)
                except:
                    continue
    
    # 디버깅을 위한 출력
    print(f"Downloaded lexicon size: {len(lexicon)} words")
    print("Sample words with emotions:")
    test_words = ['amazing', 'caring', 'happy', 'sad', 'angry']
    for word in test_words:
        if word in lexicon:
            print(f"{word}: {lexicon[word]}")
    
    return lexicon

def get_word_color(word, lexicon):
    """단어의 감정에 따라 색상 반환"""
    word = word.lower()  # 입력 단어도 소문자로 변환
    emotions = lexicon.get(word, set())
    
    # 디버깅을 위한 출력
    if word in ['amazing', 'caring', 'happy', 'good', 'bad']:
        print(f"Word: {word}, Emotions: {emotions}")
    
    if 'positive' in emotions and 'negative' not in emotions:
        return '#2ECC71'  # 초록색 (긍정)
    elif 'negative' in emotions and 'positive' not in emotions:
        return '#E74C3C'  # 빨간색 (부정)
    else:
        return '#FFD700'  # 노란색 (중립)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_and_save_wordcloud(words, title, output_path, lexicon):
    # 단어 빈도수 계산
    word_freq = Counter(words)
    
    # color_func 정의
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return get_word_color(word, lexicon)
    
    # 워드클라우드 생성
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        max_words=100,
        color_func=color_func,
        prefer_horizontal=0.7
    ).generate_from_frequencies(word_freq)
    
    # 그래프 생성
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    
    # 범례 추가
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ECC71', label='Positive'),
        Patch(facecolor='#FFD700', label='Neutral'),
        Patch(facecolor='#E74C3C', label='Negative')
    ]
    plt.legend(handles=legend_elements, loc='lower right')
    
    # 이미지 저장
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # NRC Lexicon 다운로드
    print("Downloading NRC Lexicon...")
    lexicon = download_nrc_lexicon()
    
    # JSON 파일 로드
    female_words = load_json_file('outputs/gender/female.json')
    male_words = load_json_file('outputs/gender/male.json')
    
    # 워드클라우드 생성 및 저장
    print("Generating female wordcloud...")
    create_and_save_wordcloud(
        female_words, 
        'Female Word Cloud', 
        'outputs/gender/female_wordcloud.png',
        lexicon
    )
    
    print("Generating male wordcloud...")
    create_and_save_wordcloud(
        male_words, 
        'Male Word Cloud', 
        'outputs/gender/male_wordcloud.png',
        lexicon
    )

if __name__ == "__main__":
    main()

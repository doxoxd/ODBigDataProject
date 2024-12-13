import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc
import platform
import numpy as np
import os

# Matplotlib 백엔드 설정
matplotlib.use('Agg')  # Flask 환경에서 필수

# 한글 폰트 설정
if platform.system() == 'Windows':
    # 윈도우의 경우
    font_path = "C:/Windows/Fonts/malgun.ttf"  # 맑은 고딕 경로
elif platform.system() == 'Darwin':
    # MacOS의 경우
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
else:
    # 리눅스의 경우 (예: Ubuntu)
    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

def visualize_grouped_data_with_gender(administrative_code, output_dir ='static/graph'):
    """
    특정 행정동 코드를 기준으로 데이터를 그룹별로 시각화.
    직장 인구수는 남녀 비율 그래프로만 출력.

    Parameters:
        administrative_code (int): 필터링할 행정동 코드

    Returns:
        None: 그룹별 데이터 또는 남녀 비율 그래프 출력
    """
    # 고정된 파일 경로
    file_path = './통합_위경도_클러스터.csv'

    # 데이터 로드
    data = pd.read_csv(file_path, encoding='UTF-8')

    # 특정 행정동 데이터 필터링
    filtered_data = data[data['행정동_코드_명'] == administrative_code]
    print(filtered_data)
    if filtered_data.empty:
        print(f"행정동 코드 명 {administrative_code}에 해당하는 데이터가 없습니다.")
        return

    # 그룹화 정의
    groups = {
        "직장 인구수": ['총_직장_인구_수', '남성_직장_인구_수', '여성_직장_인구_수',
                       '연령대_10_직장_인구_수', '연령대_20_직장_인구_수', '연령대_30_직장_인구_수',
                       '연령대_40_직장_인구_수', '연령대_50_직장_인구_수', '연령대_60_이상_직장_인구_수',
                       '남성연령대_10_직장_인구_수', '남성연령대_20_직장_인구_수', '남성연령대_30_직장_인구_수',
                       '남성연령대_40_직장_인구_수', '남성연령대_50_직장_인구_수', '남성연령대_60_이상_직장_인구_수',
                       '여성연령대_10_직장_인구_수', '여성연령대_20_직장_인구_수', '여성연령대_30_직장_인구_수',
                       '여성연령대_40_직장_인구_수', '여성연령대_50_직장_인구_수', '여성연령대_60_이상_직장_인구_수'],
        "유동 인구수": ['총_유동인구_수', '남성_유동인구_수', '여성_유동인구_수',
                       '연령대_10_유동인구_수', '연령대_20_유동인구_수', '연령대_30_유동인구_수',
                       '연령대_40_유동인구_수', '연령대_50_유동인구_수', '연령대_60_이상_유동인구_수'],
        "시간대별 유동 인구": ['시간대_00_06_유동인구_수', '시간대_06_11_유동인구_수', '시간대_11_14_유동인구_수',
                          '시간대_14_17_유동인구_수', '시간대_17_21_유동인구_수', '시간대_21_24_유동인구_수'],
        "요일별 유동 인구": ['월요일_유동인구_수', '화요일_유동인구_수', '수요일_유동인구_수',
                         '목요일_유동인구_수', '금요일_유동인구_수', '토요일_유동인구_수', '일요일_유동인구_수'],
        "매출 금액": ['당월_매출_금액', '주중_매출_금액', '주말_매출_금액',
                     '월요일_매출_금액', '화요일_매출_금액', '수요일_매출_금액',
                     '목요일_매출_금액', '금요일_매출_금액', '토요일_매출_금액', '일요일_매출_금액'],
        "시간대별 매출 금액": ['시간대_00~06_매출_금액', '시간대_06~11_매출_금액',
                           '시간대_11~14_매출_금액', '시간대_14~17_매출_금액',
                           '시간대_17~21_매출_금액', '시간대_21~24_매출_금액'],
        "성별 매출 금액": ['남성_매출_금액', '여성_매출_금액'],
        "연령대별 매출 금액": ['연령대_10_매출_금액', '연령대_20_매출_금액', '연령대_30_매출_금액',
                           '연령대_40_매출_금액', '연령대_50_매출_금액', '연령대_60_이상_매출_금액'],
        "매출 건수": ['당월_매출_건수', '주중_매출_건수', '주말_매출_건수',
                     '월요일_매출_건수', '화요일_매출_건수', '수요일_매출_건수',
                     '목요일_매출_건수', '금요일_매출_건수', '토요일_매출_건수', '일요일_매출_건수'],
        "시간대별 매출 건수": ['시간대_건수~06_매출_건수', '시간대_건수~11_매출_건수',
                           '시간대_건수~14_매출_건수', '시간대_건수~17_매출_건수',
                           '시간대_건수~21_매출_건수', '시간대_건수~24_매출_건수'],
        "성별 매출 건수": ['남성_매출_건수', '여성_매출_건수'],
        "연령대별 매출 건수": ['연령대_10_매출_건수', '연령대_20_매출_건수', '연령대_30_매출_건수',
                           '연령대_40_매출_건수', '연령대_50_매출_건수', '연령대_60_이상_매출_건수']
    }

     # 그룹별 데이터 시각화
    for group_name, columns in groups.items():
        if group_name == "직장 인구수":
            try:
                male_columns = ['남성연령대_10_직장_인구_수', '남성연령대_20_직장_인구_수', '남성연령대_30_직장_인구_수',
                                '남성연령대_40_직장_인구_수', '남성연령대_50_직장_인구_수', '남성연령대_60_이상_직장_인구_수']
                female_columns = ['여성연령대_10_직장_인구_수', '여성연령대_20_직장_인구_수', '여성연령대_30_직장_인구_수',
                                  '여성연령대_40_직장_인구_수', '여성연령대_50_직장_인구_수', '여성연령대_60_이상_직장_인구_수']
                
                male_data = filtered_data[male_columns].iloc[0].fillna(0)
                female_data = filtered_data[female_columns].iloc[0].fillna(0)

                # 인덱스 설정
                male_data.index = ['10대', '20대', '30대', '40대', '50대', '60대 이상']
                female_data.index = ['10대', '20대', '30대', '40대', '50대', '60대 이상']
                categories = ['10대', '20대', '30대', '40대', '50대', '60대 이상']
                male_data.index = categories
                female_data.index = categories


                # 총 인구수 계산
                total_population = male_data + female_data
                saved_graphs = []
                # 비율 계산
                male_ratio = np.divide(male_data, total_population, out=np.zeros_like(male_data), where=total_population != 0)
                female_ratio = np.divide(female_data, total_population, out=np.zeros_like(female_data), where=total_population != 0)

                # Stacked Bar Chart 생성
                plt.figure(figsize=(10, 6))
                plt.bar(male_data.index, male_ratio, label='남성', color='#0B1957')  # 어두운 파랑
                plt.bar(female_data.index, female_ratio, bottom=male_ratio, label='여성', color='#FA9EBC')  # 밝은 분홍

                # 텍스트 추가: 남성 막대 위에 남성 인구수, 여성 막대 위에 여성 인구수 표시
                for i, category in enumerate(categories):
                    male_value = int(male_data[i])
                    female_value = int(female_data[i])
                    plt.text(i, male_ratio[i], f"{male_value}", ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')  # 남성 막대 위
                    plt.text(i, male_ratio[i] + female_ratio[i], f"{female_value}", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')  # 여성 막대 위

                plt.title(f"{administrative_code} 연령대별 직장 인구수 남녀 비율", fontsize=16)
                plt.xlabel("연령대", fontsize=12)
                plt.ylabel("비율", fontsize=12)
                plt.ylim(0, 1.2)
                plt.legend()
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                #plt.tight_layout()
                #plt.show()

                # 파일로 저장
                graph_path = os.path.join(output_dir, f"{administrative_code}_{group_name}.png")
                plt.savefig(graph_path)
                plt.close()

                # 저장된 파일 경로 추가
                saved_graphs.append(graph_path.replace("\\", "/"))
                
                
            except Exception as e:
                print(f"직장 인구수 남녀 비율 그래프 생성 중 오류 발생: {e}")

        else:
            try:
                group_data = filtered_data[columns].iloc[0]
                plt.figure(figsize=(10, 6))
                plt.bar(group_data.index, group_data.values, color='#5784E6', edgecolor='#F4D1FF')  # 부드러운 파랑과 연보라 조합
                plt.title(f"{administrative_code} {group_name} 데이터", fontsize=16)
                plt.xlabel("항목", fontsize=12)
                plt.ylabel("값", fontsize=12)
                plt.xticks(rotation=45, fontsize=10)
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                #plt.tight_layout()
                #plt.show()
                
                # 파일로 저장
                graph_path = os.path.join(output_dir, f"{administrative_code}_{group_name}.png")
                plt.savefig(graph_path)
                plt.close()

                # 저장된 파일 경로 추가
                saved_graphs.append(graph_path.replace("\\", "/"))
            except Exception as e:
                print(f"Error in group '{group_name}': {e}")
                
    return saved_graphs

'''
def plot_age_based_score(all_pram, dest_hdong_cd, regionname):
    # 연령대별 점수 계산
    age_scores = {}
    for param in all_pram:
        age = param['age']
        score = param['score']
        if age in age_scores:
            age_scores[age].append(score)
        else:
            age_scores[age] = [score]

    # 평균 점수 계산
    for age in age_scores:
        age_scores[age] = np.mean(age_scores[age])  # 평균 계산

    # 정렬
    sorted_ages = sorted(age_scores.keys())
    sorted_scores = [age_scores[age] for age in sorted_ages]

    # 리스트로 변환 (plt.bar에 전달할 데이터 형식으로 변환)
    sorted_ages = [f"{age}0대" for age in sorted_ages]
    sorted_scores = list(sorted_scores)

    # 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_ages, sorted_scores, color='#5784E6', edgecolor='#F4D1FF')
    plt.title(f"{regionname} 연령대별 평균 점수", fontsize=16)
    plt.xlabel("연령대", fontsize=12)
    plt.ylabel("평균 점수", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 그래프 저장
    graph_path = f"web/static/gendergraph/{regionname}_age_based_score.png"
    plt.savefig(graph_path)
    plt.close()
    
    return graph_path
'''
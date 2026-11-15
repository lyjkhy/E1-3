
import json
import time


# MAC 연산 함수
def mac(input_data, filter_data):
    total = 0

    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            total += input_data[i][j] * filter_data[i][j]

    return total


print("=== Mini NPU Simulator ===")
print("=== data.json 분석 모드 ===")

# JSON 파일 읽기
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print("JSON 파일 읽기 성공!")

total_count = 0
pass_count = 0
fail_count = 0
fail_cases = []

print("\n=== 패턴 분석 결과 ===")

# 모든 패턴을 하나씩 분석
for pattern_name, pattern in data["patterns"].items():

    # 패턴 크기 확인
    size = pattern_name.split("_")[1]
    filter_size = "size_" + size

    # 해당 크기의 필터 선택
    filters = data["filters"][filter_size]
    filter_cross = filters["cross"]
    filter_x = filters["x"]

    input_data = pattern["input"]

    # MAC 연산 시간 측정
    start_time = time.perf_counter()

    for i in range(10):
        score_cross = mac(input_data, filter_cross)
        score_x = mac(input_data, filter_x)

    end_time = time.perf_counter()
    average_time = (end_time - start_time) * 1000 / 10

    # MAC 점수 비교
    if abs(score_cross - score_x) < 1e-9:
        result = "UNDECIDED"
    elif score_cross > score_x:
        result = "Cross"
    else:
        result = "X"

    # 기대 정답 확인
    expected = pattern["expected"]

    if expected in ("+", "cross"):
        expected_result = "Cross"
    elif expected == "x":
        expected_result = "X"
    else:
        expected_result = "UNKNOWN"

    # PASS / FAIL 확인
    if result == expected_result:
        test_result = "PASS"
        pass_count += 1
    else:
        test_result = "FAIL"
        fail_count += 1
        fail_cases.append(pattern_name)

    total_count += 1

    # 결과 출력
    print("\n테스트 이름:", pattern_name)
    print("Cross 점수:", score_cross)
    print("X 점수:", score_x)
    print("판정:", result)
    print("기대 정답:", expected_result)
    print("테스트 결과:", test_result)
    print(f"평균 계산 시간: {average_time:.6f} ms")
    print("--------------------")

# 최종 결과 요약
print("\n=== 최종 결과 요약 ===")
print("전체 테스트:", total_count)
print("성공:", pass_count)
print("실패:", fail_count)
print("실패한 테스트:", fail_cases)


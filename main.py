
import json
import math
import time

# 3x3 숫자 배열을 입력받는 함수

# 3x3 숫자 배열을 입력받는 함수
def input_matrix(name):
    print(f"\n{name} 입력 (숫자 3개씩, 총 3줄)")

    matrix = []

    while len(matrix) < 3:
        row = input(f"{len(matrix) + 1}행: ")

        try:
            numbers = [float(x) for x in row.split()]

            if len(numbers) != 3:
                print("입력 오류: 숫자 3개를 입력하세요.")
                continue
            if not all(math.isfinite(x) for x in numbers):
                print("입력 오류: 유한한 숫자만 입력하세요.")
                continue 

            matrix.append(numbers)

        except ValueError:
            print("입력 오류: 숫자만 입력하세요.")

    return matrix


# MAC 연산 함수
def mac(input_data, filter_data):
    total = 0

    for i in range(len(input_data)):
        for j in range(len(input_data[i])):
            total += input_data[i][j] * filter_data[i][j]

    return total


# MAC 연산 시간 측정 함수
def measure_time(input_data, filter_data):
    total_time = 0

    # MAC 연산을 10번 반복
    for i in range(10):
        start = time.perf_counter()
        mac(input_data, filter_data)
        end = time.perf_counter()

        total_time += end - start

    # 1회당 평균 실행 시간(ms)
    average_ms = total_time / 10 * 1000

    return average_ms

# 배열 크기별 성능 분석
def performance_analysis():
    print("\n=== 크기별 성능 분석 ===")
    print("크기 | 평균 시간(ms) | 연산 횟수")
    print("--------------------------------")

    for size in [3, 5, 13, 25]:
        # 해당 크기의 배열 만들기
        input_data = [[1] * size for _ in range(size)]
        filter_data = [[1] * size for _ in range(size)]

        # 평균 실행 시간 측정
        average_ms = measure_time(input_data, filter_data)

        # MAC 곱셈 횟수
        operations = size * size

        print(f"{size}x{size} | {average_ms:.6f} | {operations}")

# 사용자 직접 입력 모드
def user_mode():
    print("\n=== 직접 입력 모드 ===")

    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")
    pattern = input_matrix("입력 패턴")

    # MAC 점수 계산
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    # 점수 비교
    if abs(score_a - score_b) < 1e-9:
        result = "판정 불가"
    elif score_a > score_b:
        result = "A"
    else:
        result = "B"

    print("\n=== 계산 결과 ===")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    print("판정:", result)
    time_a = measure_time(pattern, filter_a)
    time_b = measure_time(pattern, filter_b)
    print(f"평균 계산 시간: {(time_a + time_b) / 2:.6f} ms")


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

user_mode()
performance_analysis()


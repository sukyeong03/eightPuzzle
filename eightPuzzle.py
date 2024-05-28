# 8-퍼즐 소스 코드 주석 (참고용) 
import copy #깊은 복사를 위해 사용

# 특정 퍼즐의 위치를 아무것도 없는 부분과 바꾸는 함수
def movePuzzle(puzzle, x, y, oper):
    if(oper == 'up'):
        if(x - 1 < 0):
            return None 
        else: 
            tmp = puzzle[x][y]
            puzzle[x][y] = puzzle[x-1][y]
            puzzle[x-1][y] = tmp

            return puzzle

    elif(oper == 'down'):
        if (x + 1 >= 3):
            return None 
        else:
            tmp = puzzle[x][y]
            puzzle[x][y] = puzzle[x + 1][y]
            puzzle[x + 1][y] = tmp

            return puzzle

    elif(oper == 'right'):
        if (y + 1 >= 3):
            return None 
        else:
            tmp = puzzle[x][y]
            puzzle[x][y] = puzzle[x][y + 1]
            puzzle[x][y + 1] = tmp

            return puzzle

    elif(oper == 'left'):
        if (y - 1 < 0):
            return None
        else:
            tmp = puzzle[x][y]
            puzzle[x][y] = puzzle[x][y - 1]
            puzzle[x][y - 1] = tmp

            return puzzle

# 아무것도 없는 부분의 위치를 반환하는 함수
def checkZero(puzzle):
    x, y = 0, 0
    for i in range(3): # x 0 ~ 2
        for j in range(3): # y 0 ~ 2
            if puzzle[i][j] == '0':
                x, y = i, j
    return x, y

# 노드 클래스
class Node:
    def __init__(self, data, differentVal, level):
        self.data = data # 퍼즐
        self.differentVal = differentVal # H 스코어
        self.level = level # 단계 (G 스코어)


# 현재 퍼즐과 목표 퍼즐이 다른 값을 반환 (H 스코어)
def differentValue(puzzle, goal):
    cnt = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal[i][j]:
                cnt += 1

    return cnt

# 단계 + 목표 퍼즐과 다른 수 (F score)
def f(puzzle, goal):
    return puzzle.level + differentValue(puzzle.data, goal)

def astar(puzzle):
    visit = [] # 방문한 퍼즐
    queue = [] 
    goal = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '0']] # 목표 퍼즐
    oper = ['up', 'down', 'right', 'left'] # 연산 종류
    # Node 객체 start
    start = Node(data=puzzle, differentVal=differentValue(puzzle=puzzle, goal=goal), level=0)
    # queue에 start 추가
    queue.append(start)

    while queue: # queue가 empty될 때까지
        current = queue.pop(0) # queue의 첫 번째 데이터 (F 스코어가 가장 작은 퍼즐)
        if(differentValue(current.data, goal)==0):
            visit.append(current.data)
            return visit # 현재 퍼즐이 목표값과 같은 경우 해당 단계까지 모든 퍼즐 반환
        else:
            visit.append(current.data) # 현재 퍼즐을 방문한 곳에 추가
            x, y = checkZero(current.data) # 현재 퍼즐의 0의 위치를 반환

            for op in oper: # 4번 실행
                next = movePuzzle(copy.deepcopy(current.data), x, y, op)
                # next가 현재 퍼즐과 같지 않고 0의 위치를 움질일 수 있으면
                if next not in visit and next is not None:
                    queue.append(Node(next, differentValue(next, goal), current.level + 1))
            # 오름차순으로 정렬의 기준이 f(X, goal)의 결과 값 (X는 queue에 존재하는 Node 객체)
            queue.sort(key=lambda X:f(X,goal), reverse=False)
    # aStar로 해결이 안됨
    return -1

def main():
    # 초기 퍼즐 상태
    puzzle = [['1', '2', '8'],
              ['6', '5', '4'],
              ['7', '3', '0']]

    # A* 알고리즘을 사용하여 퍼즐을 푸는 함수 호출
    result = astar(puzzle)

    # 결과 출력
    if result != -1:
        print("퍼즐을 푸는데 필요한 단계 수:", len(result) - 1)
        print("퍼즐의 이동 경로:")
        for step, puzzle_state in enumerate(result):
            print("Step", step)
            print_puzzle(puzzle_state)
            print()
    else:
        print("A* 알고리즘으로 퍼즐을 풀 수 없습니다.")

# 퍼즐 상태를 출력하는 함수
def print_puzzle(puzzle):
    for row in puzzle:
        print(" ".join(row))

if __name__ == "__main__":
    main()

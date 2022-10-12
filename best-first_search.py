import numpy as np
import time 
import psutil
import os

ROW = 4
COL = ROW + 1
GOAL_SCORE = ROW * COL / 2 # gia tri muc tieu cua ham heuristic

def h_function(domi_used): # h = dominoes used - duplicated
    score = 0
    for r in range(ROW):
        for c in range(ROW):
            if r == c: # doi voi nhung domino nam tren duong cheo chinh
                if domi_used[r][c] <= 2:
                    score += domi_used[r][c]
                else:
                    score += 2 - domi_used[r][c]
            else:
                if domi_used[r][c] <= 1:
                    score += domi_used[r][c]
                else:
                    score += 1 - domi_used[r][c]
    return score / 2

def next_state(mat, state, domi_used, row, col, step):
    if row == ROW:
        return []
    else:
        result = []
        if state[row][col] > 0:  # neu o da duoc dat vao
            if col == COL - 1:    # neu cot cuoi cung thi chuyen sang cot 0 cua dong tiep theo
                return next_state(mat, state, domi_used, row + 1, 0, step)
            else: # chuyen sang o tiep theo
                return next_state(mat, state, domi_used, row, col + 1, step)
        else:
            for i in range(2):
                if i == 0: # domino nam ngang
                    r1, c1 = row, col + 1
                    if c1 <= COL - 1: # kiem tra domino nam trong bang hay khong
                        if state[r1][c1] == 0:
                            # danh dau domino da chon
                            d = domi_used.copy()
                            s = state.copy()

                            d[mat[row][col]][mat[r1][c1]] += 1
                            d[mat[r1][c1]][mat[row][col]] += 1
                            s[row][col], s[r1][c1] = step, step

                            result.append((h_function(d), s, d, row, col, step))
                else: # domino nam doc
                    r1, c1 = row + 1, col
                    if r1 <= ROW - 1:
                        if state[r1][c1] == 0:
                            # danh dau domino da chon
                            d = domi_used.copy()
                            s = state.copy()

                            d[mat[row][col]][mat[r1][c1]] += 1
                            d[mat[r1][c1]][mat[row][col]] += 1
                            s[row][col], s[r1][c1] = step, step

                            result.append((h_function(d), s, d, row, col, step))
        return result

count = 0

def best_first_search(mat, state, domi_used):
    global count
    priorityQueue = []         # hang doi uu tien     
    element = (h_function(domi_used), state.copy(), domi_used.copy(), 0, 0, 0)
    priorityQueue.append(element)

    while priorityQueue:
        # if count % 10000 == 0:
        #     print(state)
        element = priorityQueue.pop(0)
        # priorityQueue.remove(element)
        state = element[1]
        domi_used = element[2]
        r = element[3]
        c = element[4]
        step = element[5] + 1
        print(element[1], 'with heuristic function value:', element[0])
        count += 1

        if h_function(domi_used) == GOAL_SCORE:
            print('Solved the dominosa!')
            print(state, 'after go through', count, 'states')
            break
        
        for next_element in next_state(mat, state, domi_used, r, c, step):
            priorityQueue.insert(0, next_element)
            
        priorityQueue.sort(key=lambda x:x[0], reverse=True)
        # element = max(priorityQueue, key= lambda x:x[0]) 

if __name__ == '__main__':
    # lay du lieu tu file
    mat = np.genfromtxt('input1.txt', delimiter = ' ', dtype='int32')
    state = np.zeros((ROW, COL), dtype = 'int32')       # ma tran trang thai
    domi_used = np.zeros((ROW, ROW), dtype = 'int32')   # ma tran kiem tra domino da su dung                                       
    
    start_time = time.time()
    # giai bai toan bang giai thuat bfs
    best_first_search(mat, state, domi_used)

    end_time = time.time()
    print('Time of algorithm is', (end_time - start_time), 'seconds')  
    print('Memory usage is', psutil.Process(os.getpid()).memory_info().rss, 'Bs')  

    # wb = openpyxl.load_workbook("stat.xlsx")
    # ws = wb['Sheet1']

    # r = 30
    # ws.cell(row=r, column=4).value = end_time - start_time
    # ws.cell(row=r, column=5).value = psutil.Process().memory_info().rss / (1024 * 1024)

    # wb.save("stat.xlsx")
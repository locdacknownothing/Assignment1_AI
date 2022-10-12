import numpy as np
import time 
import psutil
import os
# from lib_mem import mem_usage

ROW = 4
COL = ROW + 1

# trang thai (state, domi_used, row, col, step)
def next_state(mat, state, domi_used, row, col, step):
    if row == ROW:
        return []
    else:
        result = []
        if state[row][col] > 0:  # neu o da duoc dat vao
            if col == COL - 1:    # tai vi tri cot cuoi cung thi chuyen sang cot 0 cua dong tiep theo
                return next_state(mat, state, domi_used, row + 1, 0, step)
            else: # chuyen sang o tiep theo
                return next_state(mat, state, domi_used, row, col + 1, step)
        else:
            for i in range(2):
                if i == 0: # domino nam ngang
                    r1, c1 = row, col + 1
                    if c1 <= COL - 1: # kiem tra domino nam trong bang hay khong
                        if state[r1][c1] == 0:
                            d = domi_used.copy()
                            s = state.copy()

                            # danh dau domino da chon
                            d[mat[row][col]][mat[r1][c1]] += 1
                            d[mat[r1][c1]][mat[row][col]] += 1
                            s[row][col], s[r1][c1] = step, step

                            # luu vao danh sach trang thai tiep theo
                            result.append((s, d, row, col, step))
                else: # domino nam doc
                    r1, c1 = row + 1, col
                    if r1 <= ROW - 1: # kiem tra domino nam trong bang hay khong
                        if state[r1][c1] == 0:
                            d = domi_used.copy()
                            s = state.copy()

                            # danh dau domino da chon
                            d[mat[row][col]][mat[r1][c1]] += 1
                            d[mat[r1][c1]][mat[row][col]] += 1
                            s[row][col], s[r1][c1] = step, step

                            # luu vao danh sach trang thai tiep theo
                            result.append((s, d, row, col, step))
        return result

count = 0

def depth_first_search(mat, state, domi_used):
    global count
    stack = []  # stack luu cac trang thai di qua     
    element = (state.copy(), domi_used.copy(), 0, 0, 0)
    stack.append(element)

    while stack:

        # lay trang thai tu stack 
        element = stack.pop(len(stack) - 1)
        state = element[0]
        domi_used = element[1]
        r = element[2]
        c = element[3]
        step = element[4] + 1
        print(element[0])
        count += 1

        # neu tat ca domino deu duoc su dung thi ket thuc
        if np.all(domi_used > 0):
            print('Solved the dominosa!')
            print(state, 'after go through', count, 'states')
            # print(domi_used)
            break
        
        # them cac trang thai tiep theo cua trang thai hien tai vao stack
        for next_element in next_state(mat, state, domi_used, r, c, step):
            stack.append(next_element)

if __name__ == '__main__':
    mat = np.genfromtxt('input1.txt', delimiter = ' ', dtype='int32') # lay du lieu tu file
    state = np.zeros((ROW, COL), dtype = 'int32')       # ma tran trang thai
    domi_used = np.zeros((ROW, ROW), dtype = 'int32')   # ma tran kiem tra domino da su dung 

    start_time = time.time()
    # giai bai toan bang giai thuat dfs
    depth_first_search(mat, state, domi_used)

    end_time = time.time()
    print('Time of algorithm is', (end_time - start_time), 'seconds')
    print('Memory usage is', psutil.Process(os.getpid()).memory_info().rss, 'Bs')

    # wb = openpyxl.load_workbook("stat.xlsx")
    # ws = wb['Sheet1']

    # r = 30
    # ws.cell(row=r, column=2).value = end_time - start_time
    # ws.cell(row=r, column=3).value = psutil.Process().memory_info().rss / (1024 * 1024)

    # wb.save("stat.xlsx")
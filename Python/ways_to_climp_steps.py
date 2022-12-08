# Given a number of steps find the number of ways you can climp the steps
# eg. 2 -> 1 + 1 or 2 SO 2 ways

def check(i, n, process, pos):
    pos += i
    if pos <= n:
        process.append(i)
    elif pos > n:
        process = []
    return process, pos


def stepping(start, n, process, pos):
    sls = []
    for i in range(start, n+1):
        init = process.copy()
        init_pos = pos
        init, init_pos = check(i, n, init, init_pos)
        if init and init_pos == n and init not in sls:
            sls.append(init)
        elif init_pos < n:
            res = stepping(start, n, init, init_pos)
            sls += res
        else:
            break
    return sls


def steps(n):
    solutions = stepping(1, n, [], 0)
    return solutions



if __name__ == "__main__":
    max_steps = 5
    for i in range(max_steps):
        sls = steps(i)
        print(i, len(sls), ' --> ', sls)

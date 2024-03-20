import numpy as np

def test1():
    ddqaxis = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(np.diff(ddqaxis, axis=0))

    print(np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]))

def test2():
    ddqaxis = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    otg = lambda: None
    otg.delta_time = 1.0

    print("ddqxis[0, 0]:\n", ddqaxis[0, 0])

    dddqaxis = np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]) / otg.delta_time
    print(dddqaxis)

def test3():
    dddqaxis = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(dddqaxis)

    # dddqaxis[0, :]表示第一行的所有元素，
    # dddqaxis[-1, :]表示最后一行的所有元素。:是一个切片操作符，表示选择所有元素。
    dddqaxis[0, :] = 0.0
    dddqaxis[-1, :] = 0.0
    print(dddqaxis)

if __name__ == "__main__":
    # test1()
    # test2()
    test3()

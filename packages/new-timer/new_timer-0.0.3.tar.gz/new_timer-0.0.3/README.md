# new_timer
Calculate the program elapsed time.

### ManualTimer Example
    from new_timer.timer import ManualTimer

    timer1 = ManualTimer(string="Print 0 ~ 9999", decimal=2)

    for i in range(10):
        timer1.start()
        for i in range(99999):
            print(i)
        timer1.stop()

### AutoTimer Example
    from new_timer.timer import AutoTimer

    a = 0
    with AutoTimer("Pring 0 ~ 9999999", decimal=2)
        for i in range(9999999):
            a += i
            print(a)
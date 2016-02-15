def testfunction():
    env1 = 0
    o1 = [1,1,1]
    (env2, o1) = (env1 + 1, o1 + [2])
    (env3, o2) = (env2 + 1, o1 + [3])
    (env4, o3) = (env3 + 1, [6, 6, 6])
    print (env4, o1 + o2 + o3)
    return

testfunction()

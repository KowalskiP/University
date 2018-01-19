import AVLTree

main = do
    print $ listToTree [1..10]
    print $ heightTree (listToTree [1..10])
    let tree = insertTree (insertTree (insertTree (insertTree (insertTree (insertTree (insertTree (listToTree [2,3]) 1) 7) 1) 4) 5) 6) 8
    print tree
    let ntree = insertTree tree 2
    print ntree
    let tree = insertTree ntree 8
    print tree
    let ntree = remove 9 tree
    print ntree
    let tree = remove 7 ntree
    print tree
    let ntree = remove 8 tree
    print ntree
    print $ searchTree ntree 7
    print $ searchTree ntree 5
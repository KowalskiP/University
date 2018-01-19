module AVLTree (BinTree, remove, insertTree, heightTree, listToTree, treeToList, treeSort, searchTree) where
 
data BinTree a = Leaf | Node a (BinTree a) (BinTree a)
  deriving(Eq)
 
littleLeftRotate :: (Ord a, Eq a) => BinTree a -> BinTree a
littleLeftRotate Leaf = Leaf
littleLeftRotate (Node x Leaf Leaf) = Node x Leaf Leaf
littleLeftRotate (Node x l (Node r rl rr)) =
    Node r (Node x l rl) rr
 
littleRightRotate :: (Ord a, Eq a) => BinTree a -> BinTree a
littleRightRotate Leaf = Leaf
littleRightRotate (Node x Leaf Leaf) = Node x Leaf Leaf
littleRightRotate (Node x (Node l ll lr) r) = Node l ll (Node x lr r)
 
bigLeftRotate :: (Ord a, Eq a) => BinTree a -> BinTree a
bigLeftRotate Leaf = Leaf
bigLeftRotate (Node x Leaf Leaf) = Node x Leaf Leaf
bigLeftRotate (Node x l (Node r (Node rl rll rlr) rr)) =
    Node rl (Node x l rll) (Node r rlr rr)
 
bigRightRotate :: (Ord a, Eq a) => BinTree a -> BinTree a
bigRightRotate Leaf = Leaf
bigRightRotate (Node x Leaf Leaf) = Node x Leaf Leaf
bigRightRotate (Node x (Node l ll (Node lr lrl lrr)) r) =
    Node lr (Node l ll lrl) (Node x lrr r)
 
heightNode :: BinTree a -> BinTree a -> Int
heightNode x y = heightTree x - heightTree y
 
choseLeftBalance :: (Ord a, Eq a) => BinTree a -> BinTree a
choseLeftBalance Leaf = Leaf
choseLeftBalance (Node x Leaf Leaf) = Node x Leaf Leaf
choseLeftBalance(Node x l (Node r rl rr))
    | heightNode rl rr > 0 = bigLeftRotate(Node x l (Node r rl rr))
    | otherwise = littleLeftRotate(Node x l (Node r rl rr))
choseLeftBalance(Node x l r) = Node x l r
 
choseRigthBalance :: (Ord a, Eq a) => BinTree a -> BinTree a
choseRigthBalance Leaf = Leaf
choseRigthBalance (Node x Leaf Leaf) = Node x Leaf Leaf
choseRigthBalance(Node x (Node l ll lr) r)
    | heightNode ll lr < 0 = bigRightRotate(Node x (Node l ll lr) r)
    | otherwise = littleRightRotate(Node x (Node l ll lr) r)
choseRigthBalance(Node x l r) = Node x l r
 
balanceTree :: (Ord a, Eq a) => BinTree a -> BinTree a
--balanceTree Leaf = Leaf
balanceTree (Node x l r)  
    | heightNode l r == 2 = choseRigthBalance (Node x l r)
    | heightNode r l == 2 = choseLeftBalance (Node x l r)
    | otherwise = Node x l r
 
insTree :: (Ord a, Eq a) => BinTree a -> a -> BinTree a
insTree Leaf x = (Node x Leaf Leaf)
insTree (Node x l r) y
    | y < x = balanceTree (Node x (insTree l y) r)
    | y > x = balanceTree (Node x l (insTree r y))
    | otherwise = Node x l r
 
insertTree :: (Ord a, Eq a) => BinTree a -> a -> BinTree a
insertTree Leaf x = Node x Leaf Leaf
insertTree (Node x l r) y = insTree (Node x l r) y

remove :: (Ord a, Eq a) => a -> BinTree a -> BinTree a
remove x Leaf = Leaf
remove x node@(Node val l r)
    | x == val = removeNode node
    | x > val = balanceTree $ Node val l new_r
    | x < val = balanceTree $ Node val new_l r
    where
        new_r = remove x r
        new_l = remove x l

removeNode :: (Ord a, Eq a) => BinTree a -> BinTree a
removeNode (Node val Leaf Leaf) = Leaf
removeNode (Node val Leaf r) = r
removeNode (Node val l Leaf) = l
removeNode (Node val l r) =
    balanceTree $ Node min_val l new_r
    where
        (new_r, min_val) = removeMin r

removeMin :: (Ord a, Eq a) => BinTree a -> (BinTree a, a)
removeMin (Node val Leaf r) = (r, val)
removeMin (Node val l r) =
    (balanceTree tree, min_val)
    where
        (new_l, min_val) = removeMin l
        tree = Node val new_l r
 
listToTree :: (Ord a) => [a] -> BinTree a
listToTree xs = foldl insertTree Leaf xs
 
treeToList :: BinTree a -> [a]
treeToList Leaf = []
treeToList (Node x l r) = treeToList(l) ++ [x] ++ treeToList(r)
 
treeSort :: (Ord a) => [a] -> [a]
treeSort = treeToList.listToTree
 
searchTree:: (Ord a, Eq a) => BinTree a -> a -> Bool
searchTree Leaf _ = False
searchTree (Node x l r) y
    | x > y = searchTree l y
    | x < y = searchTree r y
    | otherwise = True
 
heightTree :: BinTree a -> Int
heightTree Leaf = 0
heightTree (Node _ l r) = max (heightTree l) (heightTree r) + 1
 
sizeTree :: BinTree a -> Int
sizeTree Leaf = 0
sizeTree (Node _ l r) = (sizeTree l) + (sizeTree r) + 1
 
instance Show a =>
    Show (BinTree a) where
          show t = "*-" ++ replace '\n' "\n: " (treeshow "" t)
            where
                treeshow pref Leaf = ""
                treeshow pref (Node x Leaf Leaf) =
                          (pshow pref x)

                treeshow pref (Node x left Leaf) =
                      (pshow pref x) ++ "\n" ++
                        (showSon pref "+--" "   " left)

                treeshow pref (Node x Leaf right) =
                  (pshow pref x) ++ "\n" ++
                  (showSon pref "+--" "   " right)

                treeshow pref (Node x left right) =
                  (pshow pref x) ++ "\n" ++
                  (showSon pref "|--" "|  " left) ++ "\n" ++
                  (showSon pref "+--" "   " right)

                showSon pref before next t =
                  pref ++ before ++ treeshow (pref ++ next) t

                pshow pref x = replace '\n' ("\n"++pref) (show x)

                replace c new string =
                    concatMap (change c new) string
                    where
                        change c new x
                          | x == c = new
                          | otherwise = x:[]
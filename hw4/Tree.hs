---------------------------------------------------------------------
-- David Wang
-- CAS CS 320, Fall 2015
-- Assignment 4
-- Tree.hs
--

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show)

twigs :: Tree -> Integer
twigs(Leaf) = 0
twigs(Twig) = 1
twigs(Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)

branches :: Tree -> Integer
branches(Branch t1 t2 t3) = branches(t1) + branches(t2) + branches(t3) + 1
branches(_) = 0

width :: Tree -> Integer
width(Leaf) = 1
width(Twig) = 1
width(Branch t1 t2 t3) = width(t1) + width(t2) + width(t3)

perfect :: Tree -> Bool
perfect(Twig) = False
perfect(Leaf) = True
perfect(Branch t1 t2 t3) = (t3 == t2) && (t1 == t2) && (t1 == t3) && perfect(t1) && perfect(t2) && perfect(t3)

degenerate :: Tree -> Bool
degenerate(Twig) = True
degenerate(Leaf) = True
degenerate(Branch (Branch t1 t2 t3) (Branch t4 t5 t6) _) = False
degenerate(Branch (Branch t1 t2 t3) _ (Branch t4 t5 t6)) = False
degenerate(Branch _ (Branch t1 t2 t3) (Branch t4 t5 t6)) = False
degenerate(Branch t1 t2 t3) = degenerate(t1) && degenerate(t2) && degenerate(t3)

infinite :: Tree
infinite = Branch Leaf infinite Leaf


--eof
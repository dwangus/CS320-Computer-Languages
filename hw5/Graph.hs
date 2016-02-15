---------------------------------------------------------------------
-- David Wang
-- CAS CS 320, Fall 2015
-- Assignment 5 
-- Graph.hs
--

module Graph where

data Graph a =
    Choices a (Graph a, Graph a)
  | Outcome a
  deriving (Eq, Show)

class State a where
  outcome :: a -> Bool
  choices :: a -> (a, a)

mapTuple :: (a -> b) -> (a, a) -> (b, b)
mapTuple f (x, y) = ((f x), (f y))

state :: (Graph a) -> a
state (Choices x (_,_)) = x
state (Outcome y) = y


-- If states can be compared, then graphs containing
-- those states can be compared by comparing the
-- states in the respective root nodes.
instance Ord a => Ord (Graph a) where
  g <  h = (state g) < (state h)
  g <= h = (state g) <= (state h)
  
graph :: State a => a -> Graph a
graph someState = 
  if (outcome (someState)) == True then 
    (Outcome (someState))
  else
    (Choices someState (mapTuple graph (choices someState)))

depths :: Integer -> Graph a -> [Graph a]
depths 0 someGraph = [someGraph]
depths deep (Choices someGraph (child1,child2)) = (depths (deep - 1) child1) ++ (depths (deep - 1) child2)
depths deep (Outcome someGraph) = []

fold :: State a => (a -> b) -> (a -> (b, b) -> b) -> Graph a -> b
fold o c (Outcome a) = o a
fold o c (Choices a (b1,b2)) = c a ((fold o c b1),(fold o c b2))

outcomes :: State a => Graph a -> [Graph a]
outcomes someGraph = fold (\o -> [Outcome o]) (\c (c1,c2) -> c1++c2) someGraph
--eof
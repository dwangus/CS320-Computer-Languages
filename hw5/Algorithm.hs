---------------------------------------------------------------------
-- David Wang, Collaborated w/ Jennifer Tsui
-- CAS CS 320, Fall 2015
-- Assignment 5 
-- Algorithm.hs
--
-- Issues:
--		-fit

{-# LANGUAGE FlexibleInstances #-}
module Algorithm where
import Graph
import Data.List

type Algorithm a = Graph a -> Graph a


-- Complete Problem #4, parts (a-f).
greedy :: Ord a => Algorithm a
greedy (Choices _ (child1, child2)) = min child1 child2

patient :: Ord a => Integer -> Algorithm a
patient someInteger someGraph = minimum (depths someInteger someGraph)

optimal :: (State a, Ord a) => Algorithm a
optimal someGraph = minimum (outcomes someGraph)

metaCompose :: Algorithm a -> Algorithm a -> Algorithm a
metaCompose func1 func2 someGraph = func2 (func1 someGraph)

metaRepeat :: Integer -> Algorithm a -> Algorithm a
metaRepeat 0 func someGraph = someGraph
metaRepeat someInteger func someGraph = metaRepeat (someInteger-1) func (func someGraph)

metaGreedy :: Ord a => Algorithm a -> Algorithm a -> Algorithm a
metaGreedy func1 func2 someGraph = min (func2 someGraph) (func1 someGraph)

-- Problem #4, part (g).
impatient :: Ord a => Integer -> Algorithm a
impatient n g = (metaRepeat n greedy) g
--Pro: Impatient has half as many function invocations as Patient (as patient does it for both branches
--		of every Choices tuple, and thus takes up less stack space -- and it is faster than Patient in terms
--		of run-time, since it checks only a square root of the time it takes patient at the same depth)
--Con: Because impatient only traverses one of every two siblings, compared to patient's traversal of 
--		all siblings up to a certain depth, impatient is not necessarily "correct" up to a certain depth,
--		whereas patient is necessarily right (as it checks all descendants up to a certain depth) up to
--		a certain depth -- especially because, with regards to the function definitions not necessarily
--		pertaining to State classes, the Type a can be an Integer -->
--		ExampleGraph: Choices 3 (Choices 1 (Outcome 1, Outcome 1), Choices 2 (Outcome 0, Outcome 0))
-- 		Invoking (impatient 2 ExampleGraph) vs. (patient 2 ExampleGraph) returns Outcome 1 vs. Outcome 0,
--		the former not the correct solution for this graph, and the latter the necessarily correct solution
--		up to that depth on the entire graph.


---------------------------------------------------------------------
-- Problem #5 (extra credit).
instance Ord a => Ord (Algorithm a) where
  greedy <= _ = True
  impatient < patient = True
  patient < optimal = True
  {-
  (patient someInteger1) < (impatient someInteger2) = (someInteger1 < someInteger2)
  (patient n1) <= (impatient n2) = (n1 <= n2)
  (patient n) < optimal = True
  (patient n) <= optimal = True
  (impatient n) < optimal = True
  (impatient n) <= optimal = True-}
instance Eq a => Eq (Algorithm a) where
  greedy == _ = False
  patient == _ = False
  impatient == _ = False
  optimal == _ = False

fit :: (Ord a) => Graph a -> [Algorithm a] -> Algorithm a
fit someGraph someList = minimumBy (compare) someList
---------------------------------------------------------------------
-- Problem #6 (extra extra credit).

-- An embedded language for algorithms.
data Alg =
    Greedy
  | Patient Integer
  | Impatient Integer
  | Optimal
  | MetaCompose Alg Alg
  | MetaRepeat Integer Alg
  | MetaGreedy Alg Alg
  | MaxDepth
  deriving (Eq, Show)

interpret :: (State a, Ord a) => Alg -> Algorithm a
interpret Greedy = greedy
interpret (Patient someInteger) = (patient someInteger)
interpret (Impatient someInteger) = (impatient someInteger)
interpret Optimal = optimal
interpret (MetaCompose alg1 alg2) = (metaCompose (interpret alg1) (interpret alg2))
interpret (MetaRepeat someInteger alg) = (metaRepeat someInteger (interpret alg))
interpret (MetaGreedy alg1 alg2) = (metaGreedy (interpret alg1) (interpret alg2))

data Time =
    N Integer 
  | Infinite
  deriving (Eq, Show)

instance Num Time where
  fromInteger n = N n
  Infinite + _ = Infinite
  _ + Infinite = Infinite
  (N a) + (N b) = N (a + b)
  Infinite * _ = Infinite
  _ * Infinite = Infinite
  (N a) * (N b) = N (a + b)
 
performance :: Alg -> Time
performance Greedy = N 1
performance (Patient n) = N (n^2)
performance (Impatient n) = (N n)
performance (Optimal) = Infinite
performance (MetaCompose alg1 alg2) = (performance alg1) + (performance alg2)
performance (MetaRepeat n alg1) = (N n) * (performance alg1)
performance (MetaGreedy alg1 alg2) = (performance alg1) + (performance alg2) + (N 1)

--eof
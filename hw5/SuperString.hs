---------------------------------------------------------------------
-- David Wang
-- CAS CS 320, Fall 2015
-- Assignment 5 
-- SuperString.hs
--

module SuperString where

import Data.List (isPrefixOf)
import Graph
import Algorithm

data SuperString =
    SuperStr String [String]
  deriving (Eq, Show)

-- To merge two strings, take the longest suffix of the first string
-- that overlaps with the second, and replace it with the second string.
merge :: String -> String -> String
merge (x:xs) ys  = if isPrefixOf (x:xs) ys then ys else x:(merge xs ys)
merge []     ys  = ys


instance Ord SuperString where
  (SuperStr s1 _) < (SuperStr s2 _) = length(s1) < length(s2)
  (SuperStr s1 _) <= (SuperStr s2 _) = length(s1) <= length(s2)

instance State SuperString where
  outcome (SuperStr _ []) = True
  outcome (SuperStr _ _) = False
  choices (SuperStr str (first:rest)) = (SuperStr (merge str first) rest, SuperStr (merge first str) rest)  


--eof
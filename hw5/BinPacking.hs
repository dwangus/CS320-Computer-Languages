---------------------------------------------------------------------
-- David Wang
-- CAS CS 320, Fall 2015
-- Assignment 5 
-- BinPacking.hs
--

module BinPacking where

import Graph
import Algorithm

type Item = Integer
type Bin = Integer

data BinPacking =
    BinPack Bin Bin [Item]
  deriving (Eq, Show)


instance Ord BinPacking where
  (BinPack bin1 bin2 _) < (BinPack bin3 bin4 _) = abs(bin1 - bin2) < abs(bin3 - bin4)
  (BinPack bin1 bin2 _) <= (BinPack bin3 bin4 _) = abs(bin1 - bin2) <= abs(bin3 - bin4)

instance State BinPacking where
  outcome (BinPack _ _ []) = True
  outcome (BinPack _ _ _) = False
  choices (BinPack bin1 bin2 (first:rest)) = (BinPack (bin1 + first) bin2 rest, BinPack bin1 (bin2 + first) rest)


--eof
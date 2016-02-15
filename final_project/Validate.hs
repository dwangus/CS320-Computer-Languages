--David Wang
--CS320 Fall 2015
--Lapets

module Exhaustive where

import Error
import AbstractSyntax
import Parse
import TypeCheck
import Interpret
import Compile
import Machine

type Height = Integer
type Quantity = Integer
{-
helper :: (Exp -> Exp -> Exp) -> [Exp] -> [Exp]
helper And [] = []
helper Or [] = []
helper And (x:xs) = [(And (Value True) x)] ++ [(And (Value False) x)] ++ [(And (Variable X) x)] ++ [(And (Variable Y) x)] ++ (helper And xs)
helper Or (x:xs) = [(Or (Value True) x)] ++ [(Or (Value False) x)] ++ [(Or (Variable X) x)] ++ [(Or (Variable Y) x)] ++ (helper Or xs)

helper2 :: (Exp -> Stmt -> Stmt) -> Integer -> [Stmt]
helper2 (Assign X) num = concat([(Assign X (ex) (st)) | ex <- (expexhaust (num - 1)), st <- (exhaustive (num - 1))])
helper2 (Assign Y) num = concat([(Assign Y (ex) (st)) | ex <- (expexhaust (num - 1)), st <- (exhaustive (num - 1))])
helper2 (Print) num = concat([(Print (ex) (st)) | ex <- (expexhaust (num - 1)), st <- (exhaustive (num - 1))])

helper2 :: (Exp -> Stmt -> Stmt) -> Integer -> [Stmt]
helper2 (Assign X) num = [(Assign X (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]
helper2 (Assign Y) num = [(Assign Y (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]
helper2 (Print) num = [(Print (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]

expexhaust :: Integer -> [Exp]
expexhaust 0 = []
expexhaust 1 = [Variable X, Variable Y, Value True, Value False]
expexhaust somenum = if somenum < 0 then [] else
  (expexhaust (somenum - 1)) ++ (concat [(And (e1) (e2)) | e1 <- (expexhaust 1), e2 <- (expexhaust (somenum - 1))])  ++ (concat [(Or (e1) (e2)) | e1 <- (expexhaust 1), e2 <- (expexhaust (somenum - 1))])
-}
class Exhaustive a where
  exhaustive :: Integer -> [a]
--exhaustive takes an integer and returns a list containing EVERY abstract syntax tree having height equal to or less than that integer
--  (every leaf node (values, variables, or End) is of height 1, and every other node that has children is one level higher than its maximum-height child)
--concat :: [[a]] -> [a] might be helpful
instance Exhaustive Stmt where
  exhaustive 0 = []
  exhaustive 1 = [End]
--exhaustive somenum = if somenum < 0 then [] else (helper2 (Assign X) somenum) ++ (helper2 (Assign Y) somenum) ++ (helper2 (Print) somenum)
  exhaustive num = if num < 0 then [] else
    [(Assign X (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]
    ++[(Assign Y (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]
    ++[(Print (ex) (st)) | ex <- ((exhaustive (num - 1)) :: [Exp]), st <- ((exhaustive (num - 1)) :: [Stmt])]

instance Exhaustive Exp where
  exhaustive 0 = []
  exhaustive 1 = [Variable X, Variable Y, Value True, Value False]
  exhaustive somenum = if somenum < 0 then [] else
    (exhaustive (somenum - 1)) ++ [(And (e1) (e2)) | e1 <- ((exhaustive 1) :: [Exp]), e2 <- ((exhaustive (somenum - 1)) :: [Exp])]  ++ [(Or (e1) (e2)) | e1 <- ((exhaustive 1) :: [Exp]), e2 <- ((exhaustive (somenum - 1)) :: [Exp])]
--(exhaustive (somenum - 1)) ++ (helper And (exhaustive (somenum - 1))) ++ (helper Or (exhaustive (somenum - 1)))
--(exhaustive (somenum - 1)) ++ (concat [ <- (exhaustive (somenum - 1))]) ++ (concat [ <- (exhaustive (somenum - 1))])
--map (\c -> (And (Value True) (c))) (exhaustive (somenum - 1))
--map (\c -> (And (Value False) (c))) (exhaustive (somenum - 1))
--map (\c -> (And (Variable X) (c))) (exhaustive (somenum - 1))
--map (\c -> (And (Variable Y) (c))) (exhaustive (somenum - 1))
--map (\c -> (Or (Value True) (c))) (exhaustive (somenum - 1))
--map (\c -> (Or (Value False) (c))) (exhaustive (somenum - 1))
--map (\c -> (Or (Variable X) (c))) (exhaustive (somenum - 1))
--map (\c -> (Or (Variable Y) (c))) (exhaustive (somenum - 1))

take' :: Integer -> [a] -> [a]
take' 0 _ = []
take' n (x:xs) = x:(take' (n-1) xs)
take' _ _      = []

validate :: Height -> Quantity -> Bool
validate n k = 
  (length[behavior | behavior <-((take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid]) :: [Stmt]), compileSimulate(behavior) == (liftErr converts (interpret(behavior)))]) == 
  (length(take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid]))
--			11			7			5			2				1			3						4						6					8						10					9			  12
--(length[behavior | behavior <-((take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid]) :: [Stmt]), compileSimulate(behavior) == (liftErr converts (interpret(behavior)))]) == 
--												<--13-->
--(length(take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid]))

--length of all those at depth n w/ filter for compileSimulate == interpret
validate2 :: Height -> Int
validate2 n = 
  length[behavior | behavior <- ([stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid] :: [Stmt]), compileSimulate(behavior) == (liftErr converts (interpret(behavior)))]
--length of all those w/o filter for compileSimulate == interpret
validate3 :: Height -> Int
validate3 n = 
  length[behavior | behavior <- ([stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid] :: [Stmt])]
--length of all possible abstract syntax trees, even if not well-typed
validate4 :: Height -> Int
validate4 n = 
  length[behavior | behavior <- ([stm | stm <- ((exhaustive n) :: [Stmt])] :: [Stmt])]
-- map :: (a     -> b      ) -> [a]              -> [b]
-- map :: (Value -> Integer) -> [Value] = Output -> [Integer] = Buffer
--converts :: Output -> Buffer
--length [behavior | behavior <-((take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid]) :: [Stmt]), compileSimulate(behavior) == ((liftErr converts) interpret(behavior))] == length(take' k [stm | stm <- ((exhaustive n) :: [Stmt]), (check [] stm) == Result TyVoid])

--tokenizeParse :: String -> ErrorOr Stmt
--check :: TypeEnvironment -> a -> ErrorOr Type
--compileSimulate  :: Stmt -> ErrorOr Buffer
complete :: String -> ErrorOr Buffer
complete somestring = if joinErr(liftErr (check []) (tokenizeParse somestring)) == Result TyVoid then joinErr(liftErr compileSimulate (tokenizeParse somestring)) else getOut2 (joinErr(liftErr (typeCheck) (tokenizeParse somestring)))
--complete _ = TypeError "Complete for Problem 4, part (d)."
getOut2 :: ErrorOr a -> ErrorOr Buffer
getOut2 (TypeError a) = TypeError a
--eof
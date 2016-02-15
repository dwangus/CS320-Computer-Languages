---------------------------------------------------------------------
-- David Wang
-- CAS CS 320, Fall 2015
-- Assignment 4
-- Interpret.hs
--

type Value = Integer
type Output = [Value]

data Term =
    Number Integer
  | Plus Term Term
  | Mult Term Term
  | Exponent Term Term
  | Max Term Term
  | Min Term Term

data Stmt =
    Print Term Stmt
  | End

evaluate :: Term -> Value
evaluate (Number x) = x
evaluate (Plus t1 t2) = evaluate(t1) + evaluate(t2)
evaluate (Mult t1 t2) = evaluate(t1) * evaluate(t2)
evaluate (Exponent t1 t2) = evaluate(t1) ^ evaluate(t2)
evaluate (Max t1 t2) = if evaluate(t1) > evaluate (t2) then evaluate(t1) else evaluate(t2)
evaluate (Min t1 t2) = if evaluate(t1) < evaluate (t2) then evaluate(t1) else evaluate(t2)

execute :: Stmt -> Output
execute(End) = []
execute(Print t something) = [evaluate(t)] ++ execute(something)

--eof
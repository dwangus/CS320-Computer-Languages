--David Wang
--CS320 Fall 2015
--Lapets

module Interpret where

import Error
import AbstractSyntax
import TypeCheck

type ValueEnvironment = [(Var, Value)]

remove2 :: ValueEnvironment -> Var -> ValueEnvironment
remove2 [] _ = []
remove2 ((vari,val):xvs) X = if vari == X then xvs else ((vari,val):(remove2 xvs X))
remove2 ((vari,val):xvs) Y = if vari == Y then xvs else ((vari,val):(remove2 xvs Y))
store2 :: ValueEnvironment -> Var -> Value -> ValueEnvironment
store2 env var val = env ++ [(var,val)]

valueVar :: Var -> ValueEnvironment -> Value
valueVar x' ((x,v):xvs) = if x == x' then v else valueVar x' xvs

evaluate :: ValueEnvironment -> Exp -> Value
--evaluate env _ = False -- Complete for Problem 2, part (b).
--evaluate env expr = fold (\var -> (valueVar var env)) (\boo -> Value boo) (\e1 e2 -> if (e1 == Value True) && (e2 == Value True) then Value True else Value False) (\e1 e2 -> if (e1 == Value True) || (e2 == Value True) then Value True else Value False) expr
evaluate env expr = fold (\var -> (valueVar var env)) (\boo -> boo) (\e1 e2 -> e1 && e2) (\e1 e2 -> e1 || e2) expr

--type Output = [Value]
execute :: ValueEnvironment -> Stmt -> (ValueEnvironment, Output)
execute env End = (env, [])
execute env (Print expr stm) = ((fst (execute env stm)) , ([evaluate env expr] ++ (snd (execute env stm))))
execute env (Assign var expr stm) = execute (store2 (remove2 env var) var (evaluate env expr)) stm

--check :: TypeEnvironment -> a -> ErrorOr Type
interpret :: Stmt -> ErrorOr Output
interpret stment = if (check [] stment == Result TyVoid) then Result (snd (execute [] stment)) else getOut (typeCheck stment)

getOut :: ErrorOr a -> ErrorOr Output
getOut (TypeError a) = TypeError a
--interpret stment = if (liftErr snd (typeCheck stment)) == Result TyVoid then Result (snd (execute [] stment)) else (liftErr snd (typeCheck stment))
--Is there a way to return, using check [] stment, ErrorOr Output instead of ErrorOr Type?
--interpret s = TypeError "Complete for Problem 2, part (c)."
--eof
--David Wang
--CS320 Fall 2015
--Lapets

module TypeCheck where

import Error
import AbstractSyntax

type TypeEnvironment = [(Var, Type)]

typeVar :: Var -> TypeEnvironment -> ErrorOr Type
typeVar x' ((x,t):xvs) = if x == x' then Result t else typeVar x' xvs
typeVar x'  _          = TypeError (show x' ++ " is not bound.")

remove :: TypeEnvironment -> Var -> TypeEnvironment
remove [] _ = []
remove ((v,t):xvs) X = if v == X then xvs else ((v,t):(remove xvs X))
remove ((v,t):xvs) Y = if v == Y then xvs else ((v,t):(remove xvs Y))
store :: TypeEnvironment -> Var -> ErrorOr Type -> TypeEnvironment
store env var (Result TyBool) = env ++ [(var,TyBool)]
store env var _ = env

class Typeable a where
  check :: TypeEnvironment -> a -> ErrorOr Type

instance Typeable Stmt where
  check env (End) = Result TyVoid
  --check env (Print expr stm) = if (check env stm == Result TyVoid) && (check env expr == Result TyBool) then Result TyVoid else TypeError "Something ain't right!"
  check env (Print expr stm) = if (check env expr == Result TyBool) then (if (check env stm == Result TyVoid) then Result TyVoid else check env stm) else check env expr
  check env (Assign var expr stm) = if (check env expr == Result TyBool) then (if (check (store (remove env var) var (check env expr)) stm == Result TyVoid) then Result TyVoid else check (store (remove env var) var (check env expr)) stm) else check env expr
    {-foldStmt  
    (\expr stm -> if (((check env stm) == Result TyVoid) && ((check env expr) == Result TyBool)) then Result TyVoid else TypeError "Something ain't right!") 
    (\var expr stm -> if (((check env expr) == Result TyBool) && (check (store (remove env var) var (check env expr)) stm == Result TyVoid)) then Result TyVoid else TypeError "Something ain't right!") 
    (\en -> Result TyVoid) 
    stmTree-}

instance Typeable Exp where
--check env exprTree = fold (\xory -> typeVar (xory) (env)) (\boo -> Result TyBool) (\e1 e2 -> if (e1 == e2) then Result TyBool else TypeError "Something's not bound!") (\e1 e2 -> if (e1 == e2) then Result TyBool else TypeError "Something's not bound!") exprTree
  check env exprTree = 
    fold 
    (\xory -> typeVar (xory) (env)) 
    (\boo -> Result TyBool) 
    (\e1 e2 -> if (e1 == Result TyBool) then (if (e2 == Result TyBool) then Result TyBool else e2) else e1) 
    (\e1 e2 -> if (e1 == Result TyBool) then (if (e2 == Result TyBool) then Result TyBool else e2) else e1) 
    exprTree

typeCheck :: Typeable a => a -> ErrorOr (a, Type)
typeCheck ast = liftErr (\t -> (ast, t)) (check [] ast) -- Pair result with its type.
--liftErr :: (a -> b) -> (ErrorOr a -> ErrorOr b)
--------------------------(b -> (a  , b)) (ErrorOr a)
--eof
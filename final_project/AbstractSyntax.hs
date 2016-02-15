--David Wang
--CS320 Fall 2015
--Lapets

module AbstractSyntax where

type Value = Bool
type Output = [Value]

data Var = X | Y deriving Eq

instance Show Var where
  show X = "x"
  show Y = "y"

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  deriving (Eq, Show)

data Type =
    TyBool
  | TyVoid
  deriving (Eq, Show)

fold :: (Var -> b) -> (Bool -> b) -> (b -> b -> b) -> (b -> b -> b) -> Exp -> b
fold var boo andd orr (Variable asd) = var asd
fold var boo andd orr (Value asd) = boo asd
fold var boo andd orr (And e1 e2) = andd (fold var boo andd orr e1) (fold var boo andd orr e2)
fold var boo andd orr (Or e1 e2) = orr (fold var boo andd orr e1) (fold var boo andd orr e2)

size :: Exp -> Integer
size expression = fold (\somevar -> 1) (\someboo -> 1) (\e1 e2 -> 1 + e1 + e2) (\e1 e2 -> 1 + e1 + e2) expression

foldStmt :: (Exp -> b -> b) -> (Var -> Exp -> b -> b) -> (Stmt -> b) -> Stmt -> b
foldStmt pri ass en (Print sexpr statem) = pri sexpr (foldStmt pri ass en statem)
foldStmt pri ass en (Assign svar sexpr statem) = ass svar sexpr (foldStmt pri ass en statem)
foldStmt pri ass en (End) = en (End)
--eof
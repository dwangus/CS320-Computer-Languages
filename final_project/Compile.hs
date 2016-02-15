--David Wang
--CS320 Fall 2015
--Lapets

module Compile where

import Error
import AbstractSyntax
import TypeCheck
import Machine

--type Value = Bool
--type Output = [Value]
--type Buffer = [Integer]

convert :: Value -> Integer
convert (True) = 1
convert (False) = 0
-- map :: (a     -> b      ) -> [a]              -> [b]
-- map :: (Value -> Integer) -> [Value] = Output -> [Integer] = Buffer
converts :: Output -> Buffer
converts oputs = (map convert oputs)

type AddressEnvironment = [(Var, Address)]

addressVar :: Var -> AddressEnvironment -> Address
addressVar x' ((x,a):xas) = if x == x' then a else addressVar x xas

class Compilable a where
  compile :: AddressEnvironment -> a -> [Instruction]

-- Variable X is permanently stored at address 7, Y @8
instance Compilable Exp where
  --compile env _ = [] -- Complete for Problem 3, part (a).
  -- size :: Exp -> Int
  compile env (And (Value True) e2) = (compile env e2) ++ [SET 1 1, MUL, SET 3 0, SET 4 2, COPY]
  compile env (And (Value False) e2) = (compile env e2) ++ [SET 1 0, MUL, SET 3 0, SET 4 2, COPY]
  compile env (And (Variable X) e2) = (compile env e2) ++ [SET 3 7, SET 4 1, COPY, MUL, SET 3 0, SET 4 2, COPY]
  compile env (And (Variable Y) e2) = (compile env e2) ++ [SET 3 8, SET 4 1, COPY, MUL, SET 3 0, SET 4 2, COPY]
  --compile env (Or (Value True) e2) = (compile env e2) ++ [SET 1 (-1), ADD, SET 3 0, SET 4 9, COPY, SET 2 1, SET 1 (-1), ADD, SET 3 0, SET 4 1, COPY, SET 3 9, SET 4 2, COPY, MUL, SET 3 0, SET 4 3, COPY, SET 1 0, SET 0 1, SET 4 2, COPY]
  compile env (Or (Value True) e2) = (compile env e2) ++ [SET 1 (-1), ADD, SET 3 0, SET 4 9, COPY, SET 1 0, SET 3 9, SET 4 2, COPY, MUL, SET 3 0, SET 4 3, COPY, SET 1 0, SET 0 1, SET 4 2, COPY]
  compile env (Or (Value False) e2) = (compile env e2) ++ [SET 1 (-1), ADD, SET 3 0, SET 4 9, COPY, SET 1 (-1), SET 3 9, SET 4 2, COPY, MUL, SET 3 0, SET 4 3, COPY, SET 1 0, SET 0 1, SET 4 2, COPY]
  compile env (Or (Variable X) e2) = (compile env e2) ++ [SET 1 (-1), ADD, SET 3 0, SET 4 9, COPY, SET 3 7, SET 4 2, COPY, SET 1 (-1), ADD, SET 3 0, SET 4 1, COPY, SET 3 9, SET 4 2, COPY, MUL, SET 3 0, SET 4 3, COPY, SET 1 0, SET 0 1, SET 4 2, COPY]
  compile env (Or (Variable Y) e2) = (compile env e2) ++ [SET 1 (-1), ADD, SET 3 0, SET 4 9, COPY, SET 3 8, SET 4 2, COPY, SET 1 (-1), ADD, SET 3 0, SET 4 1, COPY, SET 3 9, SET 4 2, COPY, MUL, SET 3 0, SET 4 3, COPY, SET 1 0, SET 0 1, SET 4 2, COPY]
  compile env (Variable X) = [SET 3 7, SET 4 2, COPY]
  compile env (Variable Y) = [SET 3 8, SET 4 2, COPY]
  compile env (Value True) = [SET 2 1]
  compile env (Value False) = [SET 2 0]
  -- the thing about or is... if you subtract 1 from everything, multiply both of them, all those candidates for True are represented as 0, and the one that's False is represented as 1...
  -- and then... you can copy that somewhere, then set 1 to 0, set 0 to 1, and then use the value obtained ^^^^ as an address for copy to obtain the actual value, copied to (4[dest. address])

  --For the heap... instead use... the program counter...?
instance Compilable Stmt where
  compile env (End) = []
  -- + (size expr)?
  -- SET 3 (compile env expr) ... should (compile env expr) be something else?
  -- Ahhh.... so the individual And was supposed to know where it was stored based on the size of the expression it was given + 1 (for where to store its result), and then print was supposed to use the size of the expression it was given to know where the
  --    And's result was stored
  compile env (Print expr stm) = (compile env expr) ++ [SET 3 2, SET 4 5, COPY] ++ (compile env stm)
  compile env (Assign X expr stm) = (compile env expr) ++ [SET 3 2, SET 4 7, COPY] ++ (compile env stm)
  compile env (Assign Y expr stm) = (compile env expr) ++ [SET 3 2, SET 4 8, COPY] ++ (compile env stm)
  --Need to be able to remove and assign variables in addressVar?

compileSimulate  :: Stmt -> ErrorOr Buffer
compileSimulate stment = if (check [] stment == Result TyVoid) then Result (simulate(compile [(X,7),(Y,8)] stment))  else getOut (typeCheck stment)

getOut :: ErrorOr a -> ErrorOr Buffer
getOut (TypeError a) = TypeError a
--Gonna wanna initialize to an AddressEnvironment of env = [(X,7),(Y,8)]

--eof
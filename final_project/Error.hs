--David Wang
--CS320 Fall 2015
--Lapets

{-
Last Things To Check: 
	-remove and store (ehh I don't really care)
	-foldStmt... I mean, idk if it works, but it looks like it's right, and my check [] Stmt seems to work
	-Typeable Exp check --> seems to work, I guess
	-typeError returned by interpret and compileSimulate
	-(Never needed to use size, typeCheck, addressVar)
-}

module Error where

data ErrorOr a =
    Result a
  | ParseError String
  | TypeError String
  deriving Show

promote :: ErrorOr a -> ErrorOr b
promote (ParseError s     ) = ParseError s
promote (TypeError s      ) = TypeError s

instance Eq a => Eq (ErrorOr a) where
  Result r1 == Result r2 = r1 == r2
  _ == _ = False
--(liftErr fst) (ErrorOr (a, [Token]))
liftErr :: (a -> b) -> (ErrorOr a -> ErrorOr b)
(liftErr func) (Result r) = Result (func r)
(liftErr func) (ParseError s) = ParseError s
(liftErr func) (TypeError t) = TypeError t
--I don't think you need recursive for joinErr --> only a case of nested 2, for when parsers calls parser
joinErr :: ErrorOr (ErrorOr a) -> ErrorOr a
joinErr (Result (Result something)) = Result something
joinErr (Result (ParseError something)) = ParseError something
joinErr (Result (TypeError something)) = TypeError something
joinErr (ParseError something) = ParseError something
joinErr (TypeError something) = TypeError something


--joinErr (ParseError (Result r)) = Result r
--joinErr (TypeError (Result r)) = Result r
--joinErr (ParseError (ParseError s1)) = joinErr (ParseError (s1))
--joinErr (ParseError (TypeError t1)) = joinErr (ParseError (t1))
--joinErr (TypeError (ParseError s2)) = joinErr (TypeError (s2))
--joinErr (TypeError (TypeError t2)) = joinErr (TypeError (t2))

--eof
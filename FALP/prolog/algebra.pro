:- include('draw.pro').

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Преобразование строки в список токенов.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

read_expr(Tokens) :- read_loop([], Tokens).
read_loop(Acc, Tokens) :-
	peek_code(C), C == 10 -> reverse(Acc, Tokens), ! ;
	read_token(Tok), read_loop([Tok | Acc], Tokens).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Ïðåîáðàçîâàíèå ñïèñêà òîêåíîâ â äåðåâî.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

power(bin(Op, X, Y)) --> factor(X), power_op(Op), power(Y).
power(E) --> factor(E).

factor(un(Op, X)) --> unary_op(Op), factor(X).
factor(num(X)) --> [X], {number(X)}.
factor(id(X)) --> [X], {atom(X)}.
factor(E) --> [punct('(')], expr(E), [punct(')')].

term(Result) --> power(Power), mul_op(Op), term(Power, Op, Result).
term(Result) --> power(Result).
term(Term, OpType, Result) --> 
	power(Power),
	mul_op(Op),
	term(bin(OpType, Term, Power), Op, Result).
term(Term, OpType, bin(OpType, Term, Power)) -->
	power(Power).

expr(Result) --> term(Term), add_op(Op), expr(Term, Op, Result).
expr(Result) --> term(Result).
expr(Expr, OpType, Result) --> 
	term(Term), 
	add_op(Op), 
	expr(bin(OpType, Expr, Term), Op, Result).
expr(Expr, OpType, bin(OpType, Expr, Term)) --> 
	term(Term).

unary_op('-') --> ['-'].
unary_op('sin') --> ['sin'].
unary_op('cos') --> ['cos'].
unary_op('tg') --> ['tg'].
unary_op('ctg') --> ['ctg'].
power_op('^') --> ['^'].
mul_op('*') --> ['*'].
mul_op('/') --> ['/'].
add_op('+') --> ['+'].
add_op('-') --> ['-'].

parse(Tree) :- read_expr(List), expr(Tree, List, []).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Óïðîùåíèå äåðåâà âûðàæåíèÿ.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

simplify(Tree, Tree) :- one_step(Tree, NewTree), Tree == NewTree, !.
simplify(Tree, Result) :- one_step(Tree, NewTree), simplify(NewTree, Result).
	
one_step(id(X), id(X)) :- !.
one_step(num(X), num(X)) :- !.
one_step(d(X), d(X)) :- !.
one_step(un(Op, X), R) :- simplify(X, X1), un_step(Op, X1, R), !.
one_step(bin(Op, X, Y), R) :- simplify(X, X1), simplify(Y, Y1), bin_step(Op, X1, Y1, R), !.

%% Правило для унарного минуса.

un_step(-, num(0), num(0)) :- !.
un_step(-, num(X), num(Y)) :- Y is -X, !.
un_step(-, bin(-, X, Y), bin(+, un(-, X), Y)) :- !.
un_step(-, bin(+, X, Y), bin(-, un(-, X), Y)) :- !.
un_step(-, un(-, X), X) :- !.
un_step(sin, num(X), num(Y)) :- Y is sin(X), !.
un_step(cos, num(X), num(Y)) :- Y is cos(X), !.
un_step(tg, num(X), num(Y)) :- Y is tg(X), !.
un_step(ctg, num(X), num(Y)) :- Y is ctg(X), !.

un_step(Op, X, un(Op, X)) :- !.

%% Правило для сложения.

bin_step(+, num(X), num(Y), num(Z)) :- Z is X + Y, !.
bin_step(+, X, num(0), X) :- !.
bin_step(+, num(0), Y, Y) :- !.

bin_step(+, X, num(Y), bin(+, num(Y), X)):-!.
bin_step(+, num(X), bin(+, num(Y), Z), bin(+, num(W), Z)):-W is X+Y, !.
bin_step(+, X, bin(+, num(Y), Z),bin(+,num(Y),bin(+,X,Z))):-!.
bin_step(+, X, X , bin(*, num(2), X)) :- !.
bin_step(+, X, bin(*, num(Y), X), bin(*, num(Z), X)) :- Z is Y + 1, !.
bin_step(+, bin(*, num(X), Z), bin(*, num(Y), Z), bin(*, num(W), Z)):- W is X+Y,!.


%% правило для вычитания.

bin_step(-, num(X), num(Y), num(Z)) :- Z is X - Y, !.
bin_step(-, X, num(0), X) :- !.
bin_step(-, num(0), Y, un(-, Y)) :- !.

bin_step(-, X, X, num(0)):-!.
bin_step(-, un(-, X), X, bin(*, num(-2), X)):-!.
bin_step(-, X, bin(*, num(Y), X), bin(*, num(Z), X)) :- Z is 1 - Y, !.
bin_step(-, bin(*, num(Y), X), X, bin(*, num(Z), X)) :- Z is Y - 1, !.
bin_step(-, bin(*, num(X), Z), bin(*, num(Y), Z), bin(*, num(W), Z)):- W is X - Y, !.
bin_step(-, num(X), bin(+, num(Z), Y), bin(-, num(W), Y)):- W is X - Z,!.
bin_step(-, bin(+, num(X), Z), num(Y), bin(+, num(W), Z)):- W is X - Y,!.
bin_step(-, num(X), bin(-, num(Z), Y), bin(+, num(W), Y)):- W is X - Z,!.
bin_step(-, bin(-, num(X), Z), num(Y), bin(-, num(W), Z)):- W is X - Y,!.
bin_step(-, num(X), bin(-, Y, num(Z)), bin(-, num(W), Y)):- W is X + Z,!.
bin_step(-, bin(-, Z, num(X)), num(Y), bin(+, num(W), Z)):- W is X - Y,!.


%% правило для умножения.

bin_step(*, num(X), num(Y), num(Z)) :- Z is X * Y, !.
bin_step(*, X, num(1), X) :- !.
bin_step(*, num(1), Y, Y) :- !.

bin_step(*, X, num(0), num(0)) :- !.
bin_step(*, num(0), X, num(0)) :- !.

bin_step(*, X, num(Y), bin(*, num(Y), X)):-!.
bin_step(*, num(X), bin(*, num(Y), Z), bin(*, num(W), Z)):-W is X*Y,!.
bin_step(*, num(X), bin(+, num(Y), Z), bin(+, num(W), bin(*, num(X), Z))):-W is X*Y,!.
bin_step(*, num(X), bin(-, num(Y), Z), bin(-, num(W), bin(*, num(X), Z))):-W is X*Y,!.
bin_step(*, num(X), bin(-, Z, num(Y)), bin(-, bin(*, num(X), Z), num(W))):-W is X*Y,!.
bin_step(*, X, bin(+, num(Y), X), bin(+, bin(*, num(Y), X), bin(^,X, num(2)))):-!.
bin_step(*, bin(+, num(Y), X), X, bin(+, bin(*, num(Y), X), bin(^,X, num(2)))):-!.
bin_step(*, bin(^, X, num(Y)), bin(+, num(Z), X), bin(+, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.
bin_step(*, bin(+, num(Z), X), bin(^, X, num(Y)), bin(+, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.
bin_step(*, bin(^, X, num(Y)), bin(-, num(Z), X), bin(-, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.
bin_step(*, bin(-, num(Z), X), bin(^, X, num(Y)), bin(-, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.
bin_step(*, bin(^, X, num(Y)), bin(-, X, num(Z)), bin(-, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.
bin_step(*, bin(-, X, num(Z)), bin(^, X, num(Y)), bin(-, bin(*, num(Z), bin(^, X, num(Y))), bin(^, X, num(W)))):-W is Y + 1,!.

bin_step(*, X, X, bin(^, X, num(2))):-!.
bin_step(*, X, bin(^, X, num(Y)), bin(^, X, num(W))):-W is Y+1,!.
bin_step(*, bin(^, X, num(Y)), X, bin(^, X, num(W))):-W is Y+1,!.
bin_step(*, bin(^, X, num(Y)), bin(^, X, num(Z)), bin(^, X, num(W))):-W is Y+Z,!.
bin_step(*, bin(*,num(Y), bin(^, X, num(Z))), bin(^, X, num(V)), bin(*, num(Y), bin(^, X, num(W)))):-W is Z+V,!.
bin_step(*, bin(*,num(Y), bin(^, X, num(Z))), bin(^, X, num(V)), bin(*, num(Y), bin(^, X, num(W)))):-W is Z+V,!.

bin_step(*, bin(^, X, num(Y)), bin(+, num(Z), bin(^, X, num(V))), bin(+, bin(*,num(Z), bin(^,X,num(Y))), bin(^, X, num(W)))):-W is Y+V,!.
bin_step(*, bin(+, num(Z), bin(^, X, num(V))), bin(^, X, num(Y)), bin(+, bin(*,num(Z), bin(^,X,num(Y))), bin(^, X, num(W)))):-W is Y+V,!.
bin_step(*, bin(^, X, num(Y)), bin(-, num(Z), bin(^, X, num(V))), bin(-, bin(*,num(Z), bin(^,X,num(Y))), bin(^, X, num(W)))):-W is Y+V,!.
bin_step(*, bin(-, num(Z), bin(^, X, num(V))), bin(^, X, num(Y)), bin(-, bin(*,num(Z), bin(^,X,num(Y))), bin(^, X, num(W)))):-W is Y+V,!.


%% Правило для деления.

bin_step(/, num(X), num(Y), num(Z)) :- Z is X / Y, !.
bin_step(/, X, num(1), X) :- !.

%% Правило для возведения.

bin_step(^, num(X), num(Y), num(Z)) :- Z is X ** Y, !.
bin_step(^, _, num(0), num(1)) :- !.
bin_step(^, X, num(1), X) :- !.

%% Прочие операции.

bin_step(Op, X, Y, bin(Op, X, Y)) :- !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Диффиринцирование
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

diff(num(_), num(0)) :- !.

diff(id(X), d(id(X))) :- !.

diff(un(sin, X), bin(*, un(cos, X), DX)) :- diff(X, DX), !.
diff(un(cos, X), bin(*, num(-1), bin(*, un(sin, X), DX))) :- diff(X, DX), !.
diff(un(tg, X), bin(*, bin(/, num(1), bin(^, un(cos, X), num(2))), DX)) :-diff(X, DX), !.
diff(un(ctg, X), bin(*, bin(/, num(-1), bin(^, un(sin, X), num(2))), DX)) :-diff(X, DX), !.

diff(bin(^, X, num(Y)), bin(*, bin(*, num(Y), bin(^, X, num(T))), DX)) :- diff(X, DX), T is Y - 1, !.

diff(bin(*, X, Y), bin(+, bin(*, DX, Y), bin(*, X, DY))) :- diff(Y, DY), diff(X, DX), !. 

diff(bin(+, X, Y), bin(+, DX, DY)) :- diff(Y, DY), diff(X, DX), !. 
diff(bin(-, X, Y), bin(-, DX, DY)) :- diff(Y, DY), diff(X, DX), !. 

diff(bin(/, X, Y), bin(/, bin(-, bin(*, DX, Y), bin(*, X, DY)), bin(^, Y, num(2)))) :- diff(Y, DY), diff(X, DX), !. 
diff(X, d(X)) :- !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Ïðåîáðàçîâàíèå äåðåâà â ñòðîêó ðåçóëüòàòà.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

priority(+, 1).
priority(-, 1).
priority(*, 2).
priority(/, 2).
priority(^, 3).

show_num(X) :-
	Y is float(X), Z is float_integer_part(Y),
	Z =:= Y -> (T is truncate(Y), write(T)) ; write(X).

show_op1(num(X)) :- show_num(X).
show_op1(id(X)) :- write(X).
show_op1(d(X)) :- write('('), show(X), write(')\'').
show_op1(X) :- write('('), show(X), write(')').

show_op2(num(X), _) :- show_num(X).
show_op2(id(X), _) :- write(X).
show_op2(d(X), _) :-  write('('), show(X), write(')\'').
show_op2(bin(Op, X, Y), N) :- priority(Op, M), M > N -> show(bin(Op, X, Y)).
show_op2(X, _) :- write('('), show(X), write(')').

show(num(X)) :- show_num(X).
show(id(X)) :- write(X).
show(d(X)) :-  write('('), show(X), write(')\'').

show(un(Op, X)) :- write(Op), show_op1(X).
show(bin(Op, X, Y)) :- priority(Op, N), show_op2(X, N), write(Op), show_op2(Y, N).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Запуск программы.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:- initialization(start).
start :- (parse(Tree) ->
  (draw(Tree), simplify(Tree, Result),
   draw(Result), show(Result), nl,
   diff(Result, DiffRes), draw(DiffRes), show(DiffRes), nl,
   simplify(DiffRes, SimpDiff), draw(SimpDiff), show(SimpDiff), nl)
  ; write('Syntax error!')), !.
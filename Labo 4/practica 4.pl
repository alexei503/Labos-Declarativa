
almacenar(0, []) :- !.

almacenar(N, [D | Resto]) :-
    N > 0,
    D is N mod 10,
    N1 is N // 10,
    almacenar(N1, Resto).

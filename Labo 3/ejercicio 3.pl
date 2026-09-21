factorial(1,1).
factorial(X,Y):-
    X>1,
    N is X-1,
    factorial(N,R),
    Y is X * R.


sumartoria(1,1).
sumartoria(X,Y):-
    X>1,
    N is X-1,
    sumartoria(N,R),
    Y is X + R.

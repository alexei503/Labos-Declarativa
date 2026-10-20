package org.example;

import java.io.InputStream;

import alice.tuprolog.Prolog;
import alice.tuprolog.SolveInfo;
import alice.tuprolog.Theory;

public class Connection {  
    private final Prolog engine = new Prolog();  

    public Connection() throws Exception {  
        try (InputStream in = getClass().getResourceAsStream("/calculo.pl")) {  
            if (in == null) {
                throw new IllegalStateException("No se encontró calculo.pl en resources");  
            }
            engine.setTheory(new Theory(in));  
        }  
    }  

    public String consultar(String predicado, String expresion) throws Exception {  
        // Construye la consulta: sumar(5 + 3, R). o restar(10 - 4, R).
        SolveInfo info = engine.solve(predicado + "(" + expresion + ", R).");  
        return info.isSuccess() ? info.getTerm("R").toString() : "Sin solución para esa expresión";  
    }  
}
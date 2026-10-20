import os

# Definir la estructura de directorios y archivos con su contenido
archivos = {
    "pom.xml": """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>prolog-example</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>it.unibo.alice.tuprolog</groupId>
            <artifactId>tuprolog</artifactId>
            <version>3.3.0</version>
        </dependency>
    </dependencies>
</project>""",

    "src/main/java/org/example/Main.java": """package org.example;

import org.example.screen.Window;
import javax.swing.SwingUtilities;

public class Main {
    public static void main(String[] args) throws Exception {
        Connection motor = new Connection();
        SwingUtilities.invokeLater(() -> new Window(motor).setVisible(true));
    }
}""",

    "src/main/java/org/example/Connection.java": """package org.example;

import alice.tuprolog.Prolog;
import alice.tuprolog.Theory;
import alice.tuprolog.SolveInfo;
import java.io.InputStream;

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
        SolveInfo info = engine.solve(predicado + "(x, " + expresion + ", R).");  
        return info.isSuccess() ? info.getTerm("R").toString() : "Sin solución para esa expresión";  
    }  
}""",

    "src/main/java/org/example/screen/Theme.java": """package org.example.screen;

import java.awt.Color;
import java.awt.Font;

public final class Theme {  
    private Theme() {}  

    public static final Color BG     = new Color(0x1E1F29);  
    public static final Color CARD   = new Color(0x2A2B3A);  
    public static final Color BORDER = new Color(0x3A3C52);  
    public static final Color TEXT   = new Color(0xF2F3F8);  
    public static final Color MUTED  = new Color(0x9096B0);  
    public static final Color BLUE   = new Color(0x6C8CFF);  
    public static final Color GREEN  = new Color(0x3DDC97);  
    public static final Color RED    = new Color(0xFF6B6B);  
    public static final Color AMBER  = new Color(0xFFC857);  

    public static Font sans(int estilo, int tamano) {  
        return new Font(Font.SANS_SERIF, estilo, tamano);  
    }  

    public static Font mono(int estilo, int tamano) {  
        return new Font(Font.MONOSPACED, estilo, tamano);  
    }  
}""",

    "src/main/java/org/example/screen/Window.java": """package org.example.screen;

import org.example.Connection;
import org.example.screen.components.Buttons;
import org.example.screen.components.PanelResult;
import org.example.screen.components.TextField;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.datatransfer.StringSelection;

public class Window extends JFrame {  
    private static final String[] EJEMPLOS = {  
        "x", "log(x)", "3*x^2", "2^x"  
    };  
    private final TextField txtEntrada = new TextField("Ej: 5*x^2");  
    private final PanelResult panelResultado = new PanelResult();  
    private final JLabel lblEstado = new JLabel(" ");  

    public Window(Connection motor) {  
        super("Cálculo simbólico en Prolog");  
        txtEntrada.addActionListener(e -> ejecutar(motor, "d"));  

        JPanel contenido = new JPanel();  
        contenido.setLayout(new BoxLayout(contenido, BoxLayout.Y_AXIS));  
        contenido.setOpaque(false);  

        agregar(contenido, etiqueta("Función f(x)"), 6);  
        agregar(contenido, txtEntrada, 8);  
        agregar(contenido, crearEjemplos(), 18);  
        agregar(contenido, crearBotones(motor), 22);  
        agregar(contenido, panelResultado, 10);  
        agregar(contenido, crearPie(), 0);  

        JPanel raiz = new JPanel(new BorderLayout(0, 20));  
        raiz.setBackground(Theme.BG);  
        raiz.setBorder(new EmptyBorder(24, 28, 24, 28));  
        raiz.add(crearEncabezado(), BorderLayout.NORTH);  
        raiz.add(contenido, BorderLayout.CENTER);  

        setContentPane(raiz);  
        setMinimumSize(new Dimension(660, 520));  
        pack();  
        setDefaultCloseOperation(EXIT_ON_CLOSE);  
        setLocationRelativeTo(null);  
    }  

    private JPanel crearEncabezado() {  
        JLabel titulo = new JLabel("Cálculo simbólico");  
        titulo.setFont(Theme.sans(Font.BOLD, 24));  
        titulo.setForeground(Theme.TEXT);  
        JLabel subtitulo = new JLabel("Derivadas e integrales resueltas con reglas en Prolog");  
        subtitulo.setFont(Theme.sans(Font.PLAIN, 13));  
        subtitulo.setForeground(Theme.MUTED);  

        JPanel p = new JPanel();  
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));  
        p.setOpaque(false);  
        p.add(titulo);  
        p.add(Box.createVerticalStrut(4));  
        p.add(subtitulo);  
        return p;  
    }  

    private JPanel crearEjemplos() {  
        JPanel p = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 0));  
        p.setOpaque(false);  
        JLabel lbl = new JLabel("Ejemplos:");  
        lbl.setForeground(Theme.MUTED);  
        lbl.setFont(Theme.sans(Font.PLAIN, 12));  
        p.add(lbl);  

        for (String ej : EJEMPLOS) {  
            Buttons chip = new Buttons(ej, Theme.CARD, Theme.TEXT, 12, 6, 11);  
            chip.addActionListener(e -> {  
                txtEntrada.setText(ej);  
                txtEntrada.requestFocusInWindow();  
            });  
            p.add(chip);  
        }  
        return p;  
    }  

    private JPanel crearBotones(Connection motor) {  
        Buttons btnDerivar = new Buttons("Derivar", Theme.BLUE, Theme.BG, 26, 11, 14);  
        Buttons btnIntegrar = new Buttons("Integrar", Theme.GREEN, Theme.BG, 26, 11, 14);  
        btnDerivar.addActionListener(e -> ejecutar(motor, "d"));  
        btnIntegrar.addActionListener(e -> ejecutar(motor, "s"));  

        JPanel p = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));  
        p.setOpaque(false);  
        p.add(btnDerivar);  
        p.add(btnIntegrar);  
        return p;  
    }  

    private JPanel crearPie() {  
        lblEstado.setFont(Theme.sans(Font.PLAIN, 12));  
        lblEstado.setForeground(Theme.MUTED);  
        Buttons btnCopiar = new Buttons("Copiar", Theme.CARD, Theme.TEXT, 16, 7, 12);  
        btnCopiar.addActionListener(e -> copiarResultado());  

        JPanel p = new JPanel(new BorderLayout());  
        p.setOpaque(false);  
        p.add(lblEstado, BorderLayout.WEST);  
        p.add(btnCopiar, BorderLayout.EAST);  
        return p;  
    }  

    private void ejecutar(Connection motor, String pred) {  
        String entrada = txtEntrada.getText().trim();  
        String nombre = pred.equals("d") ? "Derivada" : "Integral";  
        panelResultado.setTitulo(nombre + " de f(x)");  

        if (entrada.isEmpty()) {  
            mostrar("", "Escribí una función primero.", Theme.AMBER);  
            return;  
        }  
        try {  
            String resultado = motor.consultar(pred, entrada);  
            if (resultado.startsWith("Sin solución")) {  
                mostrar("", resultado, Theme.AMBER);  
            } else {  
                mostrar(resultado, "Listo", Theme.GREEN);  
            }  
        } catch (Exception ex) {  
            mostrar("", "Expresión inválida: " + ex.getMessage(), Theme.RED);  
        }  
    }  

    private void mostrar(String resultado, String estado, Color colorEstado) {  
        panelResultado.setTexto(resultado);  
        lblEstado.setText(estado);  
        lblEstado.setForeground(colorEstado);  
    }  

    private void copiarResultado() {  
        String t = panelResultado.getTexto();  
        if (t.isEmpty()) { return; }  
        Toolkit.getDefaultToolkit().getSystemClipboard().setContents(new StringSelection(t), null);  
        lblEstado.setText("Copiado al portapapeles");  
        lblEstado.setForeground(Theme.BLUE);  
    }  

    private static void agregar(JPanel panel, JComponent c, int espacioDespues) {  
        c.setAlignmentX(Component.LEFT_ALIGNMENT);  
        panel.add(c);  
        if (espacioDespues > 0) {  
            panel.add(Box.createVerticalStrut(espacioDespues));  
        }  
    }  

    private static JLabel etiqueta(String texto) {  
        JLabel l = new JLabel(texto);  
        l.setFont(Theme.sans(Font.BOLD, 12));  
        l.setForeground(Theme.MUTED);  
        return l;  
    }  
}""",

    "src/main/java/org/example/screen/components/Buttons.java": """package org.example.screen.components;

import org.example.screen.Theme;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class Buttons extends JButton {  
    private final Color colorBase;  
    private boolean hover;  

    public Buttons(String texto, Color colorBase, Color colorTexto, int padH, int padV, int tamFuente) {  
        super(texto);  
        this.colorBase = colorBase;  
        setFont(Theme.sans(Font.BOLD, tamFuente));  
        setForeground(colorTexto);  
        setFocusPainted(false);  
        setBorderPainted(false);  
        setContentAreaFilled(false);  
        setOpaque(false);  
        setBorder(new EmptyBorder(padV, padH, padV, padH));  
        setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));  

        addMouseListener(new MouseAdapter() {  
            @Override  
            public void mouseEntered(MouseEvent e) {  
                hover = true;  
                repaint();  
            }  
            @Override  
            public void mouseExited(MouseEvent e) {  
                hover = false;  
                repaint();  
            }  
        });  
    }  

    @Override  
    protected void paintComponent(Graphics g) {  
        Graphics2D g2 = (Graphics2D) g.create();  
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);  
        Color c = colorBase;  
        if (getModel().isPressed()) {  
            c = colorBase.darker();  
        } else if (hover) {  
            c = colorBase.equals(Theme.CARD) ? Theme.BORDER : colorBase.brighter();  
        }  
        g2.setColor(c);  
        g2.fillRoundRect(0, 0, getWidth(), getHeight(), 16, 16);  
        g2.dispose();  
        super.paintComponent(g);  
    }  
}""",

    "src/main/java/org/example/screen/components/TextField.java": """package org.example.screen.components;

import org.example.screen.Theme;
import javax.swing.*;
import javax.swing.border.CompoundBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;

public class TextField extends JTextField {  
    private final String ayuda;  

    public TextField(String ayuda) {  
        super(25);  
        this.ayuda = ayuda;  
        setFont(Theme.mono(Font.PLAIN, 18));  
        setBackground(Theme.CARD);  
        setForeground(Theme.TEXT);  
        setCaretColor(Theme.TEXT);  
        setBorder(crearBorde(Theme.BORDER));  

        addFocusListener(new FocusAdapter() {  
            @Override  
            public void focusGained(FocusEvent e) {  
                setBorder(crearBorde(Theme.BLUE));  
            }  
            @Override  
            public void focusLost(FocusEvent e) {  
                setBorder(crearBorde(Theme.BORDER));  
            }  
        });  
    }  

    private static CompoundBorder crearBorde(Color color) {  
        return new CompoundBorder(  
            new LineBorder(color, 1, true),  
            new EmptyBorder(10, 14, 10, 14));  
    }  

    @Override  
    protected void paintComponent(Graphics g) {  
        super.paintComponent(g);  
        if (getText().isEmpty()) {  
            Graphics2D g2 = (Graphics2D) g.create();  
            g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);  
            g2.setColor(Theme.MUTED);  
            g2.setFont(getFont());  
            FontMetrics fm = g2.getFontMetrics();  
            int y = (getHeight() + fm.getAscent() - fm.getDescent()) / 2;  
            g2.drawString(ayuda, getInsets().left, y);  
            g2.dispose();  
        }  
    }  
}""",

    "src/main/java/org/example/screen/components/PanelResult.java": """package org.example.screen.components;

import org.example.screen.Theme;
import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.LineBorder;
import java.awt.*;

public class PanelResult extends JPanel {  
    private final JLabel lblTitulo = new JLabel("Resultado");  
    private final JTextArea txtResultado = new JTextArea(4, 30);  

    public PanelResult() {  
        super(new BorderLayout(0, 6));  
        setOpaque(false);  
        lblTitulo.setFont(Theme.sans(Font.BOLD, 12));  
        lblTitulo.setForeground(Theme.MUTED);  

        txtResultado.setEditable(false);  
        txtResultado.setLineWrap(true);  
        txtResultado.setWrapStyleWord(true);  
        txtResultado.setFont(Theme.mono(Font.PLAIN, 17));  
        txtResultado.setBackground(Theme.CARD);  
        txtResultado.setForeground(Theme.TEXT);  
        txtResultado.setCaretColor(Theme.CARD);  
        txtResultado.setBorder(new EmptyBorder(12, 14, 12, 14));  

        JScrollPane scroll = new JScrollPane(txtResultado);  
        scroll.setBorder(new LineBorder(Theme.BORDER, 1, true));  
        scroll.getViewport().setBackground(Theme.CARD);  

        add(lblTitulo, BorderLayout.NORTH);  
        add(scroll, BorderLayout.CENTER);  
    }  

    public void setTitulo(String titulo) {  
        lblTitulo.setText(titulo);  
    }  

    public void setTexto(String texto) {  
        txtResultado.setText(texto);  
    }  

    public String getTexto() {  
        return txtResultado.getText();  
    }  
}""",

    "src/main/resources/calculo.pl": """% Reglas de cálculo simbólico (ejemplo básico)
d(X, X, 1).
s(X, X, X * X).
"""
}

for ruta, contenido in archivos.items():
    directorio = os.path.dirname(ruta)
    if directorio:
        os.makedirs(directorio, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"Creado: {ruta}")

print("\\¡Estructura de carpetas y archivos creada exitosamente!")
import java.awt.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;
import javax.swing.*;


public class GraphPanel extends JPanel {

    private double Eps = 1E-323;
    private double BorderA;
    private double BorderB;
    private static int padding = 25;
    private Color lineColor = new Color(44, 102, 230, 180);
    private static final Stroke GRAPH_STROKE = new BasicStroke(2f);
    private List<Double> Y;
    private List<Double> scores;
    private int X0 = 0;
    private double Y0 = 0;

    public GraphPanel(double a, double b) {
        this.BorderA = a;
        this.BorderB = b;
        this.scores = new ArrayList<>();
        this.Y = new ArrayList<>();
        for (double i = BorderA; i < BorderB; i+=0.01) {
            this.scores.add(MathFunction(i));
            this.Y.add(MathFunction(i));
            if (i<=0) {
                this.X0++;
                this.Y0 = MathFunction(i);
            }
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        double xScale = ((double) getWidth() - 2 * padding) / (scores.size() - 1);
        double yScale = ((double) getHeight() - 2 * padding) / (getMaxScore() - getMinScore());

        List<Point> graphPoints = new ArrayList<>();
        for (int i = 0; i < scores.size(); i++) {
            int x1 = (int) (i * xScale + padding);
            int y1 = (int) ((getMaxScore() - scores.get(i)) * yScale + padding);
            graphPoints.add(new Point(x1, y1));
        }

        g2.setColor(Color.WHITE);
        g2.fillRect(padding, padding, getWidth() - (2 * padding) , getHeight() - 2 * padding);
        g2.setColor(Color.BLACK);



        if (BorderA <= 0 & BorderB >=0) {
            g2.drawLine(padding + (int)(X0*xScale), getHeight() - padding, padding + (int)(X0*xScale), padding);
        }

        Collections.sort(Y);
        Y0 = Y.indexOf(MathFunction(X0));

        if (getMinScore() <= Eps & getMaxScore() >= Eps){
            g2.drawLine(padding, getHeight() - padding + (int) (( getMinScore())*yScale-Y0), getWidth() - padding, getHeight() - padding + (int) (( getMinScore())*yScale - Y0));
        }
        else if (Math.round(getMaxScore()) == 0)
            g2.drawLine(padding , padding, getWidth() - padding, padding);
        else if (Math.round(getMinScore()) == 0)
            g2.drawLine(padding, getHeight() - padding , getWidth() - padding, getHeight() - padding);


        Polygon p = new Polygon();
        g2.setColor(lineColor);
        g2.setStroke(GRAPH_STROKE);
        for (int i = 0; i < graphPoints.size() - 1; i++) {
            p.addPoint(graphPoints.get(i).x, graphPoints.get(i).y);
        }

        g2.drawPolyline(p.xpoints,p.ypoints,p.npoints);
    }

    private double getMinScore() {
        double minScore = Double.MAX_VALUE;
        for (Double score : scores) {
            minScore = Math.min(minScore, score);
        }
        return minScore;
    }

    private double getMaxScore() {
        double maxScore = Double.MIN_VALUE;
        for (Double score : scores) {
            maxScore = Math.max(maxScore, score);
        }
        return maxScore;

    }

    public double MathFunction(double x) {
        return x*Math.cos(x*x);
    }

    private static void createAndShowGui() {
        double BorderA = -2;
        double BorderB = 5;


        GraphPanel mainPanel = new GraphPanel(BorderA, BorderB);
        mainPanel.setPreferredSize(new Dimension(800, 600));
        JFrame frame = new JFrame("DrawGraph");

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().add(mainPanel);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> createAndShowGui());
    }
}

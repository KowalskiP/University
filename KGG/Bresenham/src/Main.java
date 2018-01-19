import javax.swing.*;
import java.awt.*;
import java.util.Vector;

public class Main extends JPanel {
    // x = (a+t)^2+b
    // y = ct+d
    static int width = 800;
    static int height = 600;

    public static int A = 0;
    public static int B = -4000;
    public static int C = 1;
    public static int D = -300;

    Parabola parabola = new Parabola();

    @Override
    public void paint(Graphics g)
    {
        super.paint(g);
        g.drawLine(0, height/2, width, height/2);
        g.drawLine(width/2, 0, width/2, height);
        g.translate(width/2, height/2);
        int shiftX = B;
        int shiftY =  -A*C + D;
        g.setColor(Color.RED);
        Vector<Point> points = parabola.getBresenhamPoints();
        for(Point point : points) {
            g.drawLine(point.x + shiftX, point.y + shiftY,
                    point.x + shiftX, point.y + shiftY);

            g.drawLine(point.x + shiftX, -point.y + shiftY,
                    point.x + shiftX, -point.y + shiftY);
        }

//        g.setColor(Color.BLUE);
//        for (double t = -20; t < 20; t += 0.01) {
//            g.drawLine(
//                    (int)((A + t)* (A+t) + B),
//                    (int)(C*t+D),
//                    (int)((A + t)* (A+t) + B),
//                    (int)(C*t+D)
//            );
//        }

        super.repaint();
    }

    public static void main(String[] args) {
        Main canv = new Main();
        canv.setPreferredSize(new Dimension(width, height));

        JFrame w=new JFrame("Function");
        w.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        w.getContentPane().add(canv);
        w.pack();

        w.setLocationRelativeTo(null);
        w.setVisible(true);
    }
}
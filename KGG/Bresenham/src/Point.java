/**
 * Created by kowalski on 4/18/16.
 */
public class Point {
    public int x;
    public int y;

    Point(int x, int y){
        this.x = x;
        this.y = y;
    }

    public double getDistToLine(Line ab)
    {
        DoublePoint a = ab.a;
        DoublePoint b = ab.b;
        double A = b.y - a.y;
        double B = -b.x + a.x;
        double C = a.y*(b.x - a.x) - a.x*(b.y - a.y);
        return Math.abs(A*x + B*y + C) / Math.sqrt(A*A + B*B);
    }
}

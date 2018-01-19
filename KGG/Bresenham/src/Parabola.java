import java.util.Vector;

/**
 * Created by kowalski on 4/18/16.
 */
public class Parabola {
    DoublePoint focus;
    Point point0;
    double p;

    Line direct;

    public Parabola()
    {
        p = Main.C*Main.C / 2.0;
        point0 = new Point(0, 0);
        focus = new DoublePoint(p/2.0, 0);
        direct = new Line(new DoublePoint(-p/2.0, 100),
                new DoublePoint(-p/2, -100));
    }

    public double getDelta( Point point)
    {
        double distToFocus = focus.getDistToIntPoint(point);
        double distToDirect = point.getDistToLine(direct);
        return distToDirect - distToFocus;
    }

    public Point dVsC(Point curPoint, double deltaC) {
        Point pointD = new Point(curPoint.x, curPoint.y + 1);
        double deltaD = getDelta(pointD);
        if (Math.abs(deltaD) < Math.abs(deltaC))
            return pointD;
        return new Point(curPoint.x + 1, curPoint.y + 1);
    }

    public Point bVsC(Point curPoint, double deltaC) {
        Point pointB = new Point(curPoint.x + 1, curPoint.y);
        double deltaB = getDelta(pointB);
        if (Math.abs(deltaB) < Math.abs(deltaC))
            return pointB;
        return new Point(curPoint.x + 1, curPoint.y + 1);
    }

    public Vector<Point> getBresenhamPoints()
    {
        Vector<Point> resPoints = new Vector<>();

        Point sP = point0;
        resPoints.add(sP);

        while(sP.x < Main.width || sP.y < Main.height) {
            Point pointC = new Point(sP.x + 1, sP.y + 1);
            double deltaC = getDelta(pointC);
            if (deltaC > 0) {
                sP = dVsC(sP, deltaC);
            } else {
                sP = bVsC(sP, deltaC);
            }
            resPoints.add(sP);
        }
        return resPoints;
    }
}

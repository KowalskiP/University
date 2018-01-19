/**
 * Created by kowalski on 4/18/16.
 */
public class DoublePoint {
    public double x;
    public double y;

    DoublePoint(double x, double y){
        this.x = x;
        this.y = y;
    }

    public double getDistToIntPoint(Point point)
    {
        return Math.sqrt((point.x - x)*(point.x - x) + (point.y - y)*(point.y - y));
    }
}

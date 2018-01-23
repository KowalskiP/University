/**
 * Created by Антон on 11.10.2014.
 */
public class Vector2D implements AbstractVector {
    private double x;
    private double y;
    public double getX(){
        return x;
    }
    public double getY(){
        return y;
    }
    public Vector2D(double a, double b){
        x=a;
        y=b;
    }
    @Override
    public double scalar(AbstractVector v) {
        Vector2D v1 = (Vector2D) v;
        return x*v1.x+y*v1.y;
    }

    @Override
    public AbstractVector add(AbstractVector v) {
        Vector2D v1 = (Vector2D) v;
        return new Vector2D(x+v1.x, y+v1.y);
    }

    @Override
    public AbstractVector multiply(double factor) {
        return new Vector2D(factor*x,factor*y);
    }

    @Override
    public AbstractVector sub(AbstractVector v) {
        Vector2D v1 = (Vector2D) v;
        return new Vector2D(x-v1.x, y-v1.y);
    }

    @Override
    public double len() {
        return Math.sqrt(x*x+y*y);
    }
}

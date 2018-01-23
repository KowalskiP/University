/**
 * Created by Антон on 07.10.2014.
 */
public class Segment {
    private Vector start;
    private Vector end;
    public Segment(Vector v1, Vector v2){
        start = v1;
        end = v2;
    }
    public Vector getStart(){
        return start;
    }

    public Vector getEnd(){
        return end;
    }

    public double len(){
        Vector s = getStart();
        Vector e = getEnd();
        double s_len = s.len();
        double e_len = e.len();
        double cosin = s.scalar(e)/(s_len*e_len);
        return Math.sqrt(s_len*s_len+e_len*e_len-2*s_len*e_len*cosin);
    }

    public double distanceTo(Vector point){
        Vector s = getStart();
        Vector e = getEnd();
        Vector v = e.sub(s);
        Vector w = point.sub(s);
        double c1 = w.scalar(v);
        if (c1 <=0 ) return w.len();
        double c2 = v.scalar(v);
        if (c2 <= c1) return (e.sub(point)).len();
        double b = c1/c2;
        Vector Pb = s.add(v.multiply(b));
        return Pb.len();
    }
}

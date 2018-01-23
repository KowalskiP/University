/**
 * Created by Антон on 15.10.2014.
 */
public class gSegment<TVector extends AbstractVector> {
    private TVector start;
    private TVector end;
    public gSegment(TVector v1, TVector v2){
        start = v1;
        end = v2;
    }
    public TVector getStart(){
        return start;
    }

    public TVector getEnd(){
        return end;
    }

    public double len(){
        TVector s = getStart();
        TVector e = getEnd();
        double s_len = s.len();
        double e_len = e.len();
        double cosin = s.scalar(e)/(s_len*e_len);
        return Math.sqrt(s_len*s_len+e_len*e_len-2*s_len*e_len*cosin);
    }

    public double distanceTo(TVector point){
        TVector s = getStart();
        TVector e = getEnd();
        AbstractVector v = e.sub(s);
        AbstractVector w = point.sub(s);
        double c1 = w.scalar(v);
        if (c1 <=0 ) return w.len();
        double c2 = v.scalar(v);
        if (c2 <= c1) return (e.sub(point)).len();
        double b = c1/c2;
        AbstractVector Pb = s.add(v.multiply(b));
        return Pb.len();
    }
}

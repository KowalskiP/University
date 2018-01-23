/**
 * Created by Антон on 15.10.2014.
 */
public class nSegment {
    private AbstractVector start;
    private AbstractVector end;
    public nSegment(AbstractVector v1, AbstractVector v2){
        start = v1;
        end = v2;
    }
    public AbstractVector getStart(){
        return start;
    }

    public AbstractVector getEnd(){
        return end;
    }

    public double len(){
        AbstractVector s = getStart();
        AbstractVector e = getEnd();
        double s_len = s.len();
        double e_len = e.len();
        double cosin = 0;
        if (s_len*e_len != 0){
            cosin = s.scalar(e)/(s_len*e_len);
        }
        return Math.sqrt(s_len*s_len+e_len*e_len-2*s_len*e_len*cosin);
    }

    public double distanceTo(AbstractVector point){
        AbstractVector s = getStart();
        AbstractVector e = getEnd();
        AbstractVector v = e.sub(s);
        AbstractVector w = point.sub(s);
        double c1 = w.scalar(v);
        if (c1 <=0 ) return w.len();
        double c2 = v.scalar(v);
        if (c2 <= c1){
            AbstractVector e1 = e.sub(point);
            return e1.len();
        };
        double b = c1/c2;
        AbstractVector v1 = v.multiply(b);
        AbstractVector Pb = s.add(v1);
        return Pb.len();
    }
}


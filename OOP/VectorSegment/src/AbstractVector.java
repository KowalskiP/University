/**
 * Created by Антон on 07.10.2014.
 */
public interface AbstractVector {
    public double scalar(AbstractVector v);
    public double len();
    public AbstractVector multiply(double factor);
    public AbstractVector add(AbstractVector v);
    public AbstractVector sub(AbstractVector v);
}

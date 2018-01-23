/**
 * Created by Антон on 17.10.2014.
 */
public class Vector3D implements AbstractVector {
    public Vector3D(double m_x, double m_y, double m_z){
        x=m_x;
        y=m_y;
        z=m_z;
    }

    public double getX(){
        return x;
    }
    public double getY(){
        return y;
    }
    public double getZ(){
        return z;
    }

    @Override
    public double scalar(AbstractVector v) {
        Vector3D v1 = (Vector3D) v;
        return getX()*v1.getX()+getY()*v1.getY()+getZ()*v1.getZ();
    }

    @Override
    public double len(){
        return Math.sqrt(getX()*getX()+getY()*getY()+getZ()*getZ());
    } // длина вектора

    @Override
    public AbstractVector multiply(double factor){
        return new Vector3D(getX()*factor,getY()*factor,getZ()*factor);
    } // умножение на число

    @Override
    public AbstractVector add(AbstractVector v) {
        Vector3D v1 = (Vector3D) v;
        return new Vector3D(getX()+v1.getX(), getY()+v1.getY(), getZ()+v1.getZ());
    }

    @Override
    public AbstractVector sub(AbstractVector v) {
        Vector3D v1 = (Vector3D) v;
        return new Vector3D(getX()-v1.getX(),getY()-v1.getY(), getZ()-v1.getZ());
    }
    private double x;
    private double y;
    private double z;
}


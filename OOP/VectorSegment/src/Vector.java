/**
 * Created by Антон on 05.10.2014.
 */
public final class Vector {

    public Vector(double m_x, double m_y, double m_z){
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
    public double scalar(Vector v){
        return getX()*v.getX()+getY()*v.getY()+getZ()*v.getZ();
    } // скалярное произведение векторов
    public double len(){
        return Math.sqrt(getX()*getX()+getY()*getY()+getZ()*getZ());
    } // длина вектора
    public Vector multiply(double factor){
        return new Vector(getX()*factor,getY()*factor,getZ()*factor);
    } // умножение на число
    public Vector add(Vector v){
        return new Vector(getX()+v.getX(), getY()+v.getY(), getZ()+v.getZ());
    } // сложение векторов
    public Vector sub(Vector v){
        return new Vector(getX()-v.getX(),getY()-v.getY(), getZ()-v.getZ());
    } // вычитание векторов
    private double x;
    private double y;
    private double z;
}

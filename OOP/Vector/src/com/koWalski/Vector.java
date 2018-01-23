package com.koWalski;

public class Vector {
    public double x, y, z;

    public Vector(double a, double b, double c){
        x=a;
        y=b;
        z=c;
    }

    public Vector add(Vector other){
        return new Vector(x+other.x, y+other. y,z+other.z);
    } // сумма векторов
    public Vector sub(Vector other){
        return new Vector(x-other.x, y-other.y, z-other.z);
    } // разность
    public Vector mult(double alpha){
        return new Vector(alpha*x, alpha*y, alpha*z);
    } // умножение на скаляр
    public double scalar(Vector other){
        return x*other.x+y*other.y+z*other.z;
    } // скалярное произведение
    public double length(){
        return Math.sqrt(x*x + y*y + z*z);
    }                 // длина вектора
    public Vector cross(Vector other){
        return new Vector(y*other.z-z*other.y, x*other.z-z*other.x, x*other.y-y*other.x);
    }      // векторное произведение
}

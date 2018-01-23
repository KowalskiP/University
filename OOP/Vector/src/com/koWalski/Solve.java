package com.koWalski;
import java.util.Scanner;

/**
 * Created by amtig_000 on 26.09.2014.
 */
public class Solve {
    public static void solveOne(Point p1, Point p2, Point p3){
        Vector s = new Vector(p2.x-p1.x, p2.y-p1.y, p2.z-p1.z);
        Vector m_s = new Vector(p1.x-p2.x, p1.y-p2.y, p1.z-p2.z);
        Vector l2 = new Vector(p3.x-p2.x, p3.y-p2.y, p3.z-p2.z);
        Vector line = new Vector(p3.x-p1.x, p3.y-p1.y, p3.z-p1.z);
        if (line.scalar(s) <0){
            System.out.println(line.length());
            return;
        }
        if (l2.scalar(m_s)<0) {
            System.out.println(l2.length());
            return;
        }
        Vector cross = s.cross(line);
        System.out.println(cross.length()/s.length());
    }
    public static void solveTwo(Point p1, Point p2, Point p3){
        Vector l1 = new Vector(p2.x-p1.x,p2.y-p1.y,p2.z-p1.z);
        Vector l2 = new Vector(p3.x-p1.x,p3.y-p1.y,p3.z-p1.z);
        Vector l3 = new Vector(p3.x-p2.x,p3.y-p2.y,p3.z-p2.z);
        if (l1.scalar(l2)==0 & l1.length()==l2.length()){
            System.out.print("yes: ");
            Point p4 = new Point(p1.x+l1.x+l2.x, p1.y+l1.y+l2.y, p1.z+l1.z+l2.z);
            p4.pprint();
        }
        else if (l1.scalar(l3)==0 & l1.length()==l3.length()){
            System.out.print("yes: ");
            Point p4 = new Point(p2.x+l3.x-l1.x, p2.y+l3.y-l1.y, p2.z+l3.z-l1.z);
            p4.pprint();
        }
        else if (l2.scalar(l3)==0 & l2.length()==l3.length()){
            System.out.print("yes: ");
            Point p4 = new Point(p3.x-l3.x-l2.x, p3.y-l3.y-l2.y, p3.z-l3.z-l2.z);
            p4.pprint();
        }
        else
            System.out.println("NO");
    }

    public static void main(String []args){
        double a,b,c;
        Scanner sc = new Scanner(System.in);
        System.out.println("input points for first task:");
        System.out.print("input points for line:");
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p1 = new Point(a,b,c);
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p2 = new Point(a,b,c);
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p3 = new Point(a,b,c);
        solveOne(p1,p2,p3);
        System.out.println("input points for second task:");
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p4 = new Point(a,b,c);
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p5 = new Point(a,b,c);
        a = sc.nextDouble();
        b = sc.nextDouble();
        c = sc.nextDouble();
        Point p6 = new Point(a,b,c);
        solveTwo(p4,p5,p6);
    }
}

class Point{
    double x, y, z;
    public Point(double a, double b, double c){
        x=a;
        y=b;
        z=c;
    }
    public void pprint(){
        System.out.printf("Point (%f, %f, %f)", x, y, z);
        System.out.println();
    }
}
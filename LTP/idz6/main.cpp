#include <iostream>
#include <fstream>
#include <list>
#include <utility>
#include "math.h"
using namespace std;

fstream in("in.txt");

typedef pair<double,double> element;

void read(fstream&,list<element>&);
void write(list<element>&);
void summ(list<element>&,list<element>&,list<element>&);
void mult(double,list<element>&,list<element>&);
double at(double,list<element>&);
int main()
{
    list<element> origin,second,result;
    double a,b;
    read(in,origin); read(in,second);
    cout<<"First: "; write(origin);
    cout<<"Second: "; write(second);
    in>>a>>b;
    summ(origin,second,result);
    cout<<"Summ: "; write(result);
    result.clear();
    mult(a,second,result);
    cout<<"Mult by "<<a<<": "; write(result);
    result.clear();
    double tmp=at(b,origin);
    cout<<"Polinom at "<<b<<": "<<tmp;
    origin.clear(); second.clear();
    return 0;
}

void read(fstream& in,list<element>& a){
    double t1,t2;
    element p;
    do{
        in>>t1>>t2;
        p = make_pair(t1,t2);
        a.push_back(p);
    }while(t2!=0);
}
void write(list<element>& a){
    for (list<element>::iterator it=a.begin();it!=a.end();it++){
        element p = *it;
        if (p.first>0) cout<<'+'<<p.first<<"x^"<<p.second;
        else if (p.first<0) cout<<p.first<<"x^"<<p.second;
        else continue;
    }
    cout<<endl;
}
void summ(list<element>& a,list<element>& b,list<element>& c){
    c=a;
    list<element>::iterator i=c.begin();
    list<element>::iterator it=b.begin();
    while(it!=b.end()){
        element p1,p2;
        p1=*i; p2=*it;
        if (p1.second<p2.second) {c.insert(i,p2); it++;}
        else if (p1.second>p2.second) {i++;}
        else if (p1.first+p2.first!=0) {element p=make_pair(p1.first+p2.first,p1.second); c.insert(i,p); i=c.erase(i); it++;}
        else {i=c.erase(i); it++;}
    }
}
void mult(double n,list<element>& a,list<element>& b){
    for (list<element>::iterator it=a.begin();it!=a.end();it++){
        element p=*it;
        b.push_back(make_pair(n*p.first,p.second));
    }
}
double at(double n,list<element>&a){
    double tmp=0;
    for (list<element>::iterator it=a.begin();it!=a.end();it++){
        element p=*it;
        tmp+=p.first*pow(n,p.second);
    }
    return tmp;
}

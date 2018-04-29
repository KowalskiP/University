#include <iostream>
#include <math.h>
using namespace std;

double side_new(double side_trianlge){
    return sqrt(2)*(1-sqrt(1-side_trianlge*side_trianlge/4));
}
int main()
{
    int n=3;
    double a=sqrt(3);
    const double e=1e-15;
    double pi=a*n/2,pi2=0;
    do{
    a=side_new(a);
    cout<<"a="<<a<<endl;
    n*=2;
    pi2=pi;
    pi=a*n/2;
    cout<<"pi="<<pi<<endl;
    cout<<"pi2="<<pi2<<endl;
    }
    while (fabs(pi-pi2)>e);
    cout<<pi;
    return 0;
}

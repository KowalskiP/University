#include <iostream>

using namespace std;

int main()
{
    long long fact1=1;
    double fact2=1;
    for (int i=2;i<=20;i++) fact1*=i;
    for (int i=2;i<=20;i++) fact2*=i;
    cout<<"fact1="<<fact1<<endl;
    cout<<"fact2="<<fact2<<endl;
    if (fact1==fact2) cout<<"fact1=fact2"<<endl; else cout<<"fact1<>fact2"<<endl;

    float x=1/3;
    double y=1/3;
    if (x==y) cout<<"x=y"<<endl; else cout<<"x<>y"<<endl;
    return 0;

}

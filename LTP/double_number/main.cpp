#include <iostream>


using namespace std;

int bin(double);
void first(double,int[]);

int main(){
    double number;
    int output[64];
    cin>>number;
    first(number);
    cout<<output;
    return 0;
}

void bin(double num,int&power,int&binar1,int&binar2){
    int cel=int(num);
    double ves=num-cel;
    binar1=0,binar2=0;
    power=0;
    int k=1;
    while (cel>0){
        int temp=cel&1;
        binar1+=b*k;
        cel>>=1;
        k*=10;
        power++;
    }
    int k=1;
    while (ves>0){
        ves*=2;
        binar2+=int(ves)*k;
        ves-=int(ves);
        k*=10;
    }
}

void first(double num, int out[64]){
    int power,cel,ves;
    int temp;
    bin(fabs(num),power,cel,ves);
    if (num>0) out[0]=0; else out[0]=1;
    int new_power=0,k;
    while (power>0){
        int b=power&1;
        new_power+=b*k;
        power>>=1;
        k*=10;
    }

}

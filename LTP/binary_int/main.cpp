#include <iostream>

using namespace std;

int main()
{
    int source,output=0,k=1;
    cin>>source;
    while (source>0){
        int b=source&1;
        //cout<<b<<endl;;
        output+=b*k;
        source>>=1;
        //cout<<source<<endl;
        k*=10;
        /*if (source&1){
            output=output*10+1;
            source>>=1;
        }
        else{
            output*=10;
            source>>=1;
        }*/
    }
    cout<<output;
    return 0;
}

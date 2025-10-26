#include<iostream>
using namespace std;

int fibonacci(int n){
    if (n<=1)
        return n;
    return fibonacci(n-1) + fibonacci(n-2);
}
int main(){
    int n=7;
    cout<<fibonacci(n)<<endl;
    //print first n fibonacci numbers
    for (int i=0; i<=n; i++){
        cout<<fibonacci(i)<<" ";
    }
    cout<<endl;
    return 0;
}

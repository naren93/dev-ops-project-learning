#include<iostream>
using namespace std;
int factorial(int n){
    if(n<=1) 
        return 1;
    return n*factorial(n-1);
}
int main(){
    int num;
    cout<<"Enter a positive integer: ";
    cin>>num;
    if(num<0){  // Factorial is not defined for negative numbers
        cout<<"Factorial is not defined for negative numbers.\n";
    } else {
        int result = factorial(num);
        cout<<"Factorial of "<<num<<" is "<<result<<endl;
    }
    return 0;
}
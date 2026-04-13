#include<iostream>
using namespace std;

void changeArray(int arr[], int n){
    // changing the array
    for (int i=0; i<n; i++){
        arr[i] = arr[i] * 2;
    }
}
int main(){
    int nums[] = {5,15,22,1,-15,24};
    int size = sizeof(nums)/sizeof(nums[0]);
    cout<<"Size of the array is: "<<size<<endl;
    cout<<"Array before change: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    // passing array to function
    changeArray(nums, size);
    cout<<"Array after change: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    return 0;
}
// Note: In C++, when you pass an array to a function, you're actually passing a pointer to the first element of the array.
// This means that any changes made to the array elements within the function will directly affect the original array in the calling function.
// Therefore, arrays are effectively passed by reference in C++.
// This is different from passing primitive data types (like int, float, etc.) which are passed by value, meaning a copy of the value is made and changes do not affect the original variable.

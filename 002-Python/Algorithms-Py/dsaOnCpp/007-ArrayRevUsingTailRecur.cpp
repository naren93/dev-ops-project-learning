#include<iostream>
using namespace std;

void swap(int *a, int *b){
    int temp = *a;
    *a = *b;
    *b = temp;
}

void reverseArray(int A[], int start, int end){
    if (start < end){
        swap(&A[start], &A[end]);
        reverseArray(A, start+1, end-1);
    }
}

int main(){
    int nums[] = {5,15,22,1,-15,24};
    int size = sizeof(nums)/sizeof(nums[0]);
    cout<<"Array before reversal: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    // reversing the array using tail recursion
    reverseArray(nums, 0, size-1);
    cout<<"Array after reversal: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    return 0;
}

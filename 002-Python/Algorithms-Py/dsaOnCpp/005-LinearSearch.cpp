#include<iostream>
using namespace std;

void linearSearch(int arr[], int n, int key){
    for (int i=0; i<n; i++){
        if (arr[i] == key){
            cout<<"Element "<<key<<" found at index "<<i<<endl;
            return;
        }
    }
    cout<<"Element "<<key<<" not found in the array"<<endl;
}
void reverseArray(int arr[], int n){
    int start = 0;
    int end = n-1;
    while (start < end){
        // swap arr[start] and arr[end]
        int temp = arr[start];
        arr[start] = arr[end];
        arr[end] = temp;
        start++;
        end--;
    }
}
int main(){
    int nums[] = {5,15,22,1,-15,24};
    int size = sizeof(nums)/sizeof(nums[0]);
    // cout<<"Size of the array is: "<<size<<endl;
    // int key;
    // cout<<"Enter the element to search: ";
    // cin>>key;
    // linearSearch(nums, size, key);
    cout<<"Array before reversal: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    // reversing the array
    reverseArray(nums, size);
    cout<<"Array after reversal: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    return 0;
}

// WAF to calculate sum and product of all elements in the array
// WAF to swap the min and max number in the array
// WAF to print all unique elements in the array
// WAF to find second largest number in the array
// WAF to print intersection of two arrays

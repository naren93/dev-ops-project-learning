#include<iostream>
using namespace std;

void insertionSort(int A[], int size){
    for (int j=1; j<size; j++){
        int key = A[j];
        int i=j-1;
        while (i>=0 && A[i]>key){
            A[i+1] = A[i];
            i--;
        }
        A[i+1] = key;
    }
}

void binarySearch(int A[], int size, int item) {
    int low=0, high=size-1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (A[mid] == item) {
            cout << "Element found at index: " << mid << endl;
            return;
        }
        if (A[mid] < item) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    cout << "Element not found" << endl;
}

int main(){
    int nums[] = {5,15,22,1,-15,24};
    int size = sizeof(nums)/sizeof(nums[0]);
    cout<<"Array before sorting: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    // sorting the array
    insertionSort(nums, size);
    cout<<"Array after sorting: ";
    for (int i=0; i<size; i++){
        cout<<nums[i]<<" ";
    }
    cout<<endl;
    int key;
    cout<<"Enter the element to search: ";
    cin>>key;
    // searching the element
    binarySearch(nums, size, key);
    return 0;
}
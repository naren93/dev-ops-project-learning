#include<iostream>
using namespace std;

int main(){
    int nums[] = {5,15,22,1,-15,24};
    int size = sizeof(nums)/sizeof(nums[0]);
    cout<<"Size of the array is: "<<size<<endl;
    // smallest number in the array
    int smallest = nums[0];
    for (int i=1; i<size; i++){
        if (nums[i] < smallest){
            smallest = nums[i];
        }
    }
    cout<<"Smallest number in the array is: "<<smallest<<endl;
    // largest number in the array
    int largest = nums[0];
    for (int i=1; i<size; i++){
        if (nums[i] > largest){
            largest = nums[i];
        }
    }
    cout<<"Largest number in the array is: "<<largest<<endl;
}
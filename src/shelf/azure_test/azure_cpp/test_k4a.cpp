#include <k4a/k4a.h>
#include <iostream>

int main() {
    std::cout << "Azure Kinect SDK Test" << std::endl;

    int device_count = k4a_device_get_installed_count();
    std::cout << "Found " << device_count << " connected device(s)" << std::endl;

    if(device_count == 0){
        std::cout << "No Kinect devices found, but SDK is working !" << std::endl;
    }

    return 0;
}

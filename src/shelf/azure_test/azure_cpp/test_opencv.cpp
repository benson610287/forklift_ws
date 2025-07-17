#include <k4a/k4a.h>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

void example6_color_thresholding() {
    cout << "=== Example 6: Color Thresholding ===" << endl;
    
    // Create a colorful test image
    Mat image = Mat::zeros(300, 400, CV_8UC3);
    
    // Draw colored regions
    rectangle(image, Point(50, 50), Point(150, 150), Scalar(255, 0, 0), -1);    // Blue
    rectangle(image, Point(200, 50), Point(300, 150), Scalar(0, 255, 0), -1);   // Green
    rectangle(image, Point(50, 180), Point(150, 280), Scalar(0, 0, 255), -1);   // Red
    rectangle(image, Point(200, 180), Point(300, 280), Scalar(255, 255, 0), -1); // Cyan
    
    // Convert to HSV
    Mat hsv;
    cvtColor(image, hsv, COLOR_BGR2HSV);
    
    // Define HSV ranges for different colors
    Mat mask_blue, mask_green, mask_red;
    
    // Blue range in HSV
    inRange(hsv, Scalar(100, 50, 50), Scalar(130, 255, 255), mask_blue);
    
    // Green range in HSV  
    inRange(hsv, Scalar(40, 50, 50), Scalar(80, 255, 255), mask_green);
    
    // Red range in HSV (red wraps around in HSV)
    Mat mask_red1, mask_red2;
    inRange(hsv, Scalar(0, 50, 50), Scalar(10, 255, 255), mask_red1);
    inRange(hsv, Scalar(170, 50, 50), Scalar(180, 255, 255), mask_red2);
    mask_red = mask_red1 | mask_red2;
    
    // Apply masks to original image
    Mat result_blue, result_green, result_red;
    image.copyTo(result_blue, mask_blue);
    image.copyTo(result_green, mask_green);
    image.copyTo(result_red, mask_red);
    
    // Display results
    imshow("Original", image);
    imshow("HSV", hsv);
    imshow("Blue Objects", result_blue);
    imshow("Green Objects", result_green);
    imshow("Red Objects", result_red);
    
    cout << "Press any key to continue..." << endl;
    waitKey(0);
}


int main() {
    cout << "OpenCV Example" << endl;
    try {
        example6_color_thresholding();
    }
    catch (const Exception& e) {
        cout << "OpenCV Error: " << e.what() << endl;
        return -1;
    }

    cout << "Examples completed!" << endl;
    return 0;
}
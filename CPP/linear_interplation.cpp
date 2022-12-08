// Linear inteprolation similar to numpy.interp
// https://numpy.org/doc/stable/reference/generated/numpy.interp.html
// Perform linear interpolation and run tests.
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <stdexcept>
#include <numeric>
using namespace std;

// Linear interpolation formula: y = y1 + (y2-y1)(x - x1) / (x2-x1)
float linear(float x, float x1, float x2, float y1, float y2){
  auto ys = y2 - y1;
  auto xs = x2 - x1;
  auto xb = x - x1;
  auto y = y1 + (ys * xb / xs);
  return y;
}


// interpolation functions
float interp(std::vector<float> xRef, std::vector<float> yRef, float xQuery){
  // check sizes
  auto sizeX = xRef.size();
  auto sizeY = yRef.size();
  if ( sizeX != sizeY){
    string message = "Vector sizes are not the same: ";
    message += "xRef " + to_string(sizeX);
    message += ", yRef " + to_string(sizeY);
    throw invalid_argument(message);
  }
  if (sizeX == 0){
    throw invalid_argument("Vectors cannot be empty");
  }

  // check bounds
  float max_x = *max_element(std::begin(xRef), std::end(xRef)); 
  float min_x = *min_element(std::begin(xRef), std::end(xRef)); 
  if (xQuery > max_x){
    throw invalid_argument("xQuery ("+ to_string(xQuery) +") is larger than max X ("+ to_string(max_x) +")");
  }
  if (xQuery < min_x){
    throw invalid_argument("xQuery ("+ to_string(xQuery) +") is lower than min X ("+ to_string(min_x) +")");
  }  
  
  // created a sorted indexes in respect to X
  vector<int> indexes(sizeX);
  iota(indexes.begin(), indexes.end(), 0);
  sort(indexes.begin(), indexes.end(),
           [&xRef](int a, int b) -> bool {
                return xRef[a] < xRef[b];
            });

  // select appropriate x,y values for interpolation
  float x1,x2,y1,y2;
  int size = indexes.size() - 1;
  int index1, index2;
  auto found = false;
  // get x,y values according to the 'sorted' indexes
  for(int i = 0; i < size; ++i){
    index1 = indexes[i];
    index2 = indexes[i+1];
    x1 = xRef[index1];
    x2 = xRef[index2];
    y1 = yRef[index1];
    y2 = yRef[index2];    
    if ((xQuery >= x1) && (xQuery <=x2)){
      found = true;
      break;
    }    
  }
  // Just in case test
  if (!found){
    throw invalid_argument("Appropriate pair could not be found (Cannot happen)");
  }

  // inerpolate
  auto result = linear(xQuery,x1,x2,y1,y2);
  return result;
}

int main()
{
    // Example test data
    std::vector<float> xReference {1, 2, 3};
    std::vector<float> yReference {2, 4, 6};
    // Add tests here!

    cout<<"\nSimple cases\n";
    std::vector<float> xQs {1,1.5,2,2.5,3};
    std::vector<float> actual {2,3,4,5,6};
    int size_qs = xQs.size();
    for(int i = 0; i < size_qs; ++i){    
      auto value = interp(xReference, yReference, xQs[i]);
      cout<<"Result for x = "<<xQs[i]<<" : y = "<<value<<endl;
      if (value != actual[i]){
        cout<<" --> Test Failed"<<endl;
      }
    }    
    // Bounds Test
    cout<<"\nTest for Bounds:\n";
    xReference = {1, 2, 3};
    yReference = {2, 4, 6};    
    std::vector<float> xQs2 {0, 5};
    for(const auto& xq : xQs2){
      try {
        auto result = interp(xReference, yReference, xq);
        cout<<result<<" --> Test Failed"<<endl;
      }
      catch( const std::invalid_argument& ex ) {
          cerr <<"- Error: "<< ex.what() << endl;
      }    
    }

    // Size Test:
    cout<<"\nTest for size:\n";
    xReference = {1, 2, 3};
    yReference = {2, 4, 6, 5};
    try {
      auto result2 = interp(xReference, yReference, 2.5);
      cout<<result2<<" --> Test Failed"<<endl;
    }
    catch( const std::invalid_argument& ex ) {
         cerr <<"- Error: "<< ex.what() << endl;
    }    


    // unsorted
    xReference = {2, 3, 1};
    yReference = {4, 6, 2};
    // Add tests here!

    cout<<"\nUnsorted cases\n";
    xQs = {1,1.5,2,2.5,3};
    actual = {2,3,4,5,6};
    size_qs = xQs.size();
    for(int i = 0; i < size_qs; ++i){    
      auto value2 = interp(xReference, yReference, xQs[i]);
      cout<<"Result for x = "<<xQs[i]<<" : y = "<<value2<<endl;
      if (value2 != actual[i]){
        cout<<" --> Test Failed"<<endl;
      }
    }    


    cout<<"\nTest Empty case\n";
    xReference = {};
    yReference = {};
    try {
      auto result3 = interp(xReference, yReference, 2.5);
      cout<<result3<<" --> Test Failed"<<endl;
    }
    catch( const std::invalid_argument& ex ) {
         cerr <<"- Error: "<< ex.what() << endl;
    }    
    
}
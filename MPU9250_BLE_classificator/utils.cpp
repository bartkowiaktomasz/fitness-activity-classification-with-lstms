#include "config.h"

#include <iostream>
#include <string>
#include <algorithm>
#include <vector>

std::string softmax_to_label(std::vector<float> output){
  int argMax = std::distance(output.begin(), std::max_element(output.begin(), output.end()));
  return LABELS_NAMES[argMax];
}

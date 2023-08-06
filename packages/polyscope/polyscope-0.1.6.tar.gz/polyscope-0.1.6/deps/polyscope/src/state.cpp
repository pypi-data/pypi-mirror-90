// Copyright 2017-2019, Nicholas Sharp and the Polyscope contributors. http://polyscope.run.
#include "polyscope/polyscope.h"

namespace polyscope {

namespace state {

bool initialized = false;
double lengthScale = 1.0;
std::tuple<glm::vec3, glm::vec3> boundingBox;
glm::vec3 center{0, 0, 0};
std::map<std::string, std::map<std::string, Structure*>> structures;
std::function<void()> userCallback;
std::set<Widget*> widgets;

} // namespace state
} // namespace polyscope

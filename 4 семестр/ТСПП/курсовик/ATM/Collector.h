#pragma once
#include "Worker.h"

class Collector : 
    public Worker
{
public:
    Collector(string name, int id) : Worker(name, id) {}
    ~Collector() {}

    string getRole() const override { return "collector"; }
};


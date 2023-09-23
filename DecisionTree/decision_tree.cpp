#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <math.h>

class decisionTree
{
private:
    std::vector<std::vector<std::string>> data;
    std::vector<std::vector<std::string>> domains;

    std::string MCV;
    bool isLeaf = false;

    std::vector<bool> usedInputs;

    // a map storing the next trees
    std::map<std::string, decisionTree*> next;

    int bestHeuristicIdx = -1;
    // lower values are prefered, any double.max will never be chosen
    std::function<std::vector<double>(std::vector<std::vector<std::string>>)> hFunction;

    std::string print(int tabs, std::string splitVal)
    {
        std::string out;

        for (int i = 0; i < tabs; i++)
            out += "  ";
        out += "Val - " + splitVal;

        if (isLeaf)
            return out + "    Return - " + MCV + "    dataset size = " + std::to_string(data.size()) + "\n";

        auto h = hFunction(data);

        out += "   NextSplitIdx = " + std::to_string(this->bestHeuristicIdx) + "    h = [";
        for (auto h : hFunction(this->data))
            out += " " + std::to_string(h) + ",";
        out.pop_back();
        out += " ]";

        // out += "    h - ";
        // for (auto v : h)
        //     out += std::to_string(v) + "  ";



        out += "\n";

        for (auto [k,v] : this->next)
            out += v->print(tabs + 1, k);

        return out;
    }

    // returns a leaf node with value mcv
    decisionTree(std::string mcv) {
        isLeaf = true;
        this->MCV = mcv;
    }

    decisionTree(auto data, auto hf, std::vector<bool> usedInputs, std::vector<std::vector<std::string>> domains) {

        this->data = std::vector<std::vector<std::string>>(data);
        this->hFunction = hf;

        this->usedInputs = std::vector<bool>(usedInputs);

        this->domains = std::vector<std::vector<std::string>>(domains);

        this->MCV = getMCV();
    }

    std::string getMCV() {
        std::map<std::string, int> counter;

        for(auto entry : data) {

            if (counter.count(entry.back()) == 0)
                counter.emplace(entry.back(), 0);
            counter[entry.back()]++;
        }

        std::string bestK;
        int best = 0;

        for (auto [k, v] : counter)
            if (v > best) {
                best = v;
                bestK = k;
            }
        
        if (best == 0)
            return "";
        
        return bestK;
    }

    std::map<std::string, std::vector<std::vector<std::string>>> splitData(std::vector<std::vector<std::string>> data, int splitIdx) {
        std::map<std::string, std::vector<std::vector<std::string>>> out;

        for(auto k : domains[splitIdx])
            out.emplace(k, std::vector<std::vector<std::string>>());
        
        for (auto entry : data)
            out[entry[splitIdx]].push_back(entry);
        
        return out;
    }

public:
    // set mcv
    decisionTree(auto data, auto hf) {
        this->data = std::vector<std::vector<std::string>>(data);
        this->hFunction = hf;

        for (int i = 0; i < data[0].size() - 1; i++)
            this->usedInputs.push_back(false);


        for(auto entry : data[0])
            domains.push_back(std::vector<std::string>());

        for (auto entry : data)
            for (int i = 0; i < entry.size(); i++)
                if (std::count(domains[i].begin(), domains[i].end(), entry[i]) == 0)
                    domains[i].push_back(entry[i]);

        this->MCV = getMCV();
    }
    



    void split(int maxDepth) {
        if (isLeaf)
            return;

        if (data.size() == 0 || maxDepth == 0) {
            isLeaf = true;
            return;
        }

        bool sameOutput = true;
        for(auto entry : data)
            if (entry.back() != MCV) {
                sameOutput = false;
                break;
            }
        
        if (sameOutput) {
            isLeaf = true;
            return;
        }

        std::vector<double> h = hFunction(data);

        double best = __DBL_MAX__;
        for (int i = 0; i < usedInputs.size(); i++)
            if (!usedInputs[i] && h[i] < best) {
                bestHeuristicIdx = i;
                best = h[i];
            }

        if (bestHeuristicIdx == -1) {
            isLeaf = true;
            return;
        }

        auto subsets = splitData(data, bestHeuristicIdx);

        next = std::map<std::string, decisionTree*>();

        for(auto [k, v] : subsets) {
            decisionTree* n;
            if (v.size() == 0)
                n = new decisionTree(this->MCV);
            else
                n = new decisionTree(v, this->hFunction, this->usedInputs, domains);
            next.emplace(k, n);
            n->split(maxDepth-1);
        }
    }

    void print()
    {
        std::cout << print(0, "root");
    }
};


std::vector<double> majorityError(std::vector<std::vector<std::string>> data)
{
    std::vector<double> out;

    std::map<std::string, double> defCounter;
    std::vector<std::map<std::string, double>> counters;

    // setup the default counter to have every output as a key
    for (auto entry : data)
        if (defCounter.count(entry.back()) == 0)
            defCounter.emplace(entry.back(), 0);
    
    // add a copy of defCounter to counters for every input
    for (int i = 0; i < data[0].size() - 1; i++)
        counters.push_back(std::map<std::string, double>(defCounter));

    // count occurances
    for (auto entry : data)
        for (int i = 0; i < entry.size() - 1; i++)
            counters[i][entry[i]]++;


    for (auto counter : counters) {

        double best = 0;

        for (auto [k, v] : counter) {
            double err = abs(1.0/counter.size() - v/data.size());
            if (err > best)
                best = err;
        }
        
        // ensures no divide by 0s and better best value means lower out value
        out.push_back(best);
    }
    
    return out;
}


std::vector<double> entropy(std::vector<std::vector<std::string>> data) {
    std::vector<double> out;

    std::map<std::string, double> defCounter;
    std::vector<std::map<std::string, double>> counters;

    // setup the default counter to have every output as a key
    for (auto entry : data)
        if (defCounter.count(entry.back()) == 0)
            defCounter.emplace(entry.back(), 0);
    
    // add a copy of defCounter to counters for every input
    for (int i = 0; i < data[0].size() - 1; i++)
        counters.push_back(std::map<std::string, double>(defCounter));

    // count occurances
    for (auto entry : data)
        for (int i = 0; i < entry.size() - 1; i++)
            counters[i][entry[i]]++;

    return out;
}








int main()
{
    std::vector<std::vector<std::string>> data;

    std::fstream f;
    f.open("in.csv", std::ios::in);

    std::string line, val, tmp;

    while (f.good())
    {
        std::vector<std::string> entry;
        std::getline(f, line);
        std::stringstream ss(line);

        while (getline(ss, val, ','))
            entry.push_back(val);
            
        
        data.push_back(entry);
    }

    decisionTree root(data, &majorityError);

    root.split(5);

    root.print();


    return 0;
}
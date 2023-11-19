#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <random>
#include <iomanip>
#include <map>
#include <string>
#include <algorithm>
#include <iterator>
#include <ranges>






void generateSetCoveringInstance(int num_elements, int num_sets, double density, std::ofstream &txt_file, std::ofstream &wcnf_file) {
    txt_file << num_elements << " " << num_sets << "\n";

    std::random_device rd;
    std::mt19937 gen(rd());
    std::bernoulli_distribution bd(density);
    std::uniform_int_distribution<> ud(1, 100);


    std::vector<uint16_t> costs(num_sets);  
    std::generate(costs.begin(), costs.end(), [&] () { return ud(gen); });
    
    // Enter costs into txt file
    std::for_each(costs.begin(), costs.end(), [&,i=1] (uint16_t e) {
        txt_file << e; 
        if (i != num_sets) {
            txt_file << ' ';
        } 
    });
    txt_file << '\n';

    // Enter costs into wcnf file
    std::for_each(costs.begin(), costs.end(), [&,i=1] (uint16_t e) {
        wcnf_file << e << " " << -i << " 0\n"; 
    });


    // Create a vector to store the samples
    std::vector<bool> row(num_sets);

    for (int i = 0; i < num_elements; i++) {
        std::generate(row.begin(), row.end(), [&] () { return bd(gen); });
        
        // number of sets the element is contained in
        auto sets_contained = std::accumulate(row.begin(), row.end(), 0);
        
        // each element must be contained in at least one set in order to make the instance solvable
        if (!sets_contained){
            i--;
            continue;
        }

        // enter the row
        txt_file << sets_contained << '\n';
        wcnf_file << "h ";
        
        bool started = false;
        std::for_each(row.begin(), row.end(), [&,i=1] (bool b) mutable {
            if (b) {
                if (started) {
                    txt_file << ' ';
                }
                started = true;
                wcnf_file << i << ' '; 
                txt_file << i; 
            }

            i++;
        });
        txt_file << '\n';
        wcnf_file << "0\n";



        

    }
}

int main(int argc, char* argv[]) {
    if (argc != 6) {
        std::cerr << "Usage: " << argv[0] << " num_elements num_sets density txt_path wcnf_path\n";
        return 1;
    }

    int numElements = std::atoi(argv[1]);
    int numSets = std::atoi(argv[2]);
    double density = std::atof(argv[3]);
    std::string txt_path = argv[4];
    std::string wcnf_path = argv[5]; 

    // Open the text file
    std::ofstream txt_file(txt_path);
    if (!txt_file.is_open()) {
        std::cerr << "Error: Unable to open the output file.\n";
        return 1;
    }

    // Open the wcnf file
    std::ofstream wcnf_file(wcnf_path);
    if (!wcnf_file.is_open()) {
        std::cerr << "Error: Unable to open the output file.\n";
        return 1;
    }

    // Generate and output the set covering instance
    generateSetCoveringInstance(numElements, numSets, density, txt_file, wcnf_file);

    // Close the output file
    txt_file.close();

    return 0;
}

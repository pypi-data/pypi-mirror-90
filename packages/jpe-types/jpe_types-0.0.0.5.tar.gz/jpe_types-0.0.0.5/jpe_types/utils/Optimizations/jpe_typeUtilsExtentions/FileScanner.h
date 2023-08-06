#pragma once
#include<string>
#include <fstream>
#include <iostream>
#include <list>


std::list<int> findRefrences(std::string file, std::string val) {
		// find refences to val in file f
		std::list<int> linesFoundIn;
		int count = 0;
		int lineNumber = 0;
		std::ifstream infile;
		std::string line;
		int pos = 0;

		infile.open(file);
		while (std::getline(infile, line)) {
			if (line.find(val, pos) != std::string::npos) {
				linesFoundIn.push_back(lineNumber);
				count++;
			}
			lineNumber++;
		}
		return linesFoundIn;
	}
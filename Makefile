CXX=/usr/local/bin/g++-10
CXXFLAGS=-std=c++17 -O3 -Wall -Werror -Wextra -Wshadow -Wno-sign-compare
SYSFLAGS=-isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk

all: simulate

simulate: simulate.cc
	 $(CXX) ${CXXFLAGS} ${SYSFLAGS} -o simulate simulate.cc


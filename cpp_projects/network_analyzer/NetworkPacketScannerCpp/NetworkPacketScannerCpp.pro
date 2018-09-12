TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += src/main.cpp \
    src/net_packet_lib.cpp

INCLUDEPATH += /usr/local/include
LIBS += -L/usr/local/lib
LIBS += -lpcap
LIBS += -lpthread

HEADERS += \
    header/net_packet_lib.h

TARGET = helloworld

# qmake -o Makefile ../NetworkPacketScannerCpp.pro
# make

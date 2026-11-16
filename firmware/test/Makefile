# Decoder-Tests auf dem Rechner (ohne ESP32): make -C firmware/test

SKETCH := ../vrt240f_sniffer
BUILD  := build

test: $(BUILD)/test_decoder
	./$(BUILD)/test_decoder

$(BUILD)/test_decoder: test_decoder.cpp $(SKETCH)/vaillant_decoder.cpp $(SKETCH)/vaillant_decoder.h
	mkdir -p $(BUILD)
	$(CXX) -std=c++17 -Wall -Wextra -I$(SKETCH) -o $@ test_decoder.cpp $(SKETCH)/vaillant_decoder.cpp

clean:
	rm -rf $(BUILD)

.PHONY: test clean

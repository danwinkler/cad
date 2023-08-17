

union() {
	difference() {
		difference() {
			difference() {
				difference() {
					translate(v = [5, 5, 5]) {
						minkowski() {
							cube(size = [148, 74, 11.0000000000]);
							sphere($fn = 32, r = 5);
						}
					}
					translate(v = [0, 0, 16.0000000000]) {
						cube(size = [158, 84, 5]);
					}
				}
				translate(v = [5, 5, 5]) {
					cube(size = [148, 68, 12.0000000000]);
				}
			}
			translate(v = [39.5000000000, 84, 16.0000000000]) {
				translate(v = [-10, -1, -8]) {
					cube(size = [20, 2, 9]);
					translate(v = [0, 0, 3.1000000000]) {
						translate(v = [3.7500000000, 0, 0]) {
							rotate(a = 90, v = [1, 0, 0]) {
								cylinder(h = 9, r = 1);
							}
						}
						translate(v = [16.2500000000, 0, 0]) {
							rotate(a = 90, v = [1, 0, 0]) {
								cylinder(h = 9, r = 1);
							}
						}
					}
				}
			}
		}
		translate(v = [118.5000000000, 84, 16.0000000000]) {
			translate(v = [-10, -1, -8]) {
				cube(size = [20, 2, 9]);
				translate(v = [0, 0, 3.1000000000]) {
					translate(v = [3.7500000000, 0, 0]) {
						rotate(a = 90, v = [1, 0, 0]) {
							cylinder(h = 9, r = 1);
						}
					}
					translate(v = [16.2500000000, 0, 0]) {
						rotate(a = 90, v = [1, 0, 0]) {
							cylinder(h = 9, r = 1);
						}
					}
				}
			}
		}
	}
}
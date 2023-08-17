

union() {
	difference() {
		cube(size = [35.5000000000, 39.7500000000, 26]);
		translate(v = [2, 2, -1]) {
			cube(size = [31.5000000000, 35.7500000000, 28]);
		}
		translate(v = [17.7500000000, -0.0100000000, 13.0000000000]) {
			rotate(a = -90, v = [1, 0, 0]) {
				cylinder(h = 39.7700000000, r = 11.0000000000);
			}
		}
	}
	translate(v = [35.5000000000, 11.4500000000, 0]) {
		union() {
			cube(size = [11.9000000000, 2, 26]);
			translate(v = [9.9000000000, 0, 0]) {
				cube(size = [2, 5, 26]);
			}
			translate(v = [0, 26.3000000000]) {
				difference() {
					cube(size = [11.9000000000, 2, 26]);
					translate(v = [0, -0.0100000000, 5.5000000000]) {
						translate(v = [3, 0, 3]) {
							minkowski() {
								cube(size = [3.9000000000, 2.0200000000, 9]);
								rotate(a = 90, v = [1, 0, 0]) {
									cylinder($fn = 16, h = 2, r = 3);
								}
							}
						}
					}
				}
				translate(v = [9.9000000000, -3, 0]) {
					cube(size = [2, 5, 26]);
				}
			}
		}
	}
	translate(v = [-10.3000000000, 3.4500000000, 0]) {
		union() {
			cube(size = [10.3000000000, 2, 26]);
			translate(v = [0, 0, 0]) {
				cube(size = [2, 5, 26]);
			}
			translate(v = [0, 34.3000000000]) {
				difference() {
					cube(size = [10.3000000000, 2, 26]);
					translate(v = [2, -0.0100000000, 5.5000000000]) {
						translate(v = [3, 0, 3]) {
							minkowski() {
								cube(size = [2.3000000000, 2.0200000000, 9]);
								rotate(a = 90, v = [1, 0, 0]) {
									cylinder($fn = 16, h = 2, r = 3);
								}
							}
						}
					}
				}
				translate(v = [0, -3, 0]) {
					cube(size = [2, 5, 26]);
				}
			}
		}
	}
}
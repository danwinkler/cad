

union() {
	difference() {
		union() {
			difference() {
				difference() {
					difference() {
						difference() {
							cube(size = [83, 57, 75]);
							translate(v = [-1, 0, 55]) {
								rotate(a = 90, v = [0, 0, 1]) {
									rotate(a = 90, v = [1, 0, 0]) {
										linear_extrude(height = 85) {
											polygon(paths = [[0, 1, 2, 3, 4]], points = [[-1, 0], [5, 0], [52, 20], [52, 100], [-1, 100]]);
										}
									}
								}
							}
						}
						translate(v = [-1, -1, 55]) {
							cube(size = [4, 472, 100]);
						}
					}
					translate(v = [80, -1, 55]) {
						cube(size = [4, 472, 100]);
					}
				}
				translate(v = [-1, 54, 55]) {
					cube(size = [85, 4, 100]);
				}
			}
			translate(v = [41, 52.5000000000, 65.0000000000]) {
				sphere($fn = 20, r = 3);
			}
		}
		translate(v = [5, 5, 5]) {
			cube(size = [73, 47, 100]);
		}
	}
	translate(v = [-88, 0, 1]) {
		difference() {
			difference() {
				difference() {
					translate(v = [0, 0, 55]) {
						cube(size = [83, 57, 55]);
					}
					translate(v = [5, 5, 5]) {
						cube(size = [73, 47, 100]);
					}
				}
				translate(v = [2, 0, 55]) {
					rotate(a = 90, v = [0, 0, 1]) {
						rotate(a = 90, v = [1, 0, 0]) {
							linear_extrude(height = 79) {
								polygon(paths = [[0, 1, 2, 3]], points = [[5, -2], [55, -2], [55, 20], [5, 0]]);
							}
						}
					}
				}
			}
			translate(v = [41, 53.0000000000, 65.0000000000]) {
				sphere($fn = 20, r = 3);
			}
		}
	}
}
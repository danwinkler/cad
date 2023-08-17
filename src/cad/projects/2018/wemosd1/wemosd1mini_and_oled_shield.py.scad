

union() {
	difference() {
		difference() {
			difference() {
				difference() {
					difference() {
						difference() {
							minkowski() {
								translate(v = [2, 2, 2]) {
									cube(size = [28.6000000000, 37.2000000000, 24.0000000000]);
								}
								sphere($fn = 12, r = 2);
							}
							translate(v = [0, 0, 26.0000000000]) {
								cube(size = [32.6000000000, 41.2000000000, 3]);
							}
						}
						translate(v = [3, 3, 3]) {
							cube(size = [26.6000000000, 35.2000000000, 24.0000000000]);
						}
					}
					translate(v = [8.8000000000, -1, 6]) {
						cube(size = [15, 5, 10]);
					}
				}
				translate(v = [2, 2, 24.0000000000]) {
					cube(size = [28.6000000000, 37.2000000000, 3]);
				}
			}
			translate(v = [-0.5000000000, 7, 20]) {
				rotate(a = 90, v = [0, 1, 0]) {
					cylinder($fn = 24, h = 4, r = 3);
					translate(v = [0, 0, 2.0000000000]) {
						cylinder($fn = 24, h = 3, r = 4);
					}
				}
			}
		}
		translate(v = [32.6000000000, 7, 20]) {
			rotate(a = -90, v = [0, 1, 0]) {
				cylinder($fn = 24, h = 4, r = 3);
				translate(v = [0, 0, 2.0000000000]) {
					cylinder($fn = 24, h = 3, r = 4);
				}
			}
		}
	}
	translate(v = [3, 3, 3]) {
		difference() {
			cube(size = [6, 6, 5]);
			translate(v = [3.3000000000, 3.3000000000, 0]) {
				cylinder($fn = 12, h = 5.1000000000, r = 1.5000000000);
			}
		}
	}
	translate(v = [29.6000000000, 3, 3]) {
		scale(v = [-1, 1, 1]) {
			difference() {
				cube(size = [6, 6, 5]);
				translate(v = [3.3000000000, 3.3000000000, 0]) {
					cylinder($fn = 12, h = 5.1000000000, r = 1.5000000000);
				}
			}
		}
	}
	translate(v = [29.6000000000, 38.2000000000, 3]) {
		scale(v = [1, -1, 1]) {
			scale(v = [-1, 1, 1]) {
				difference() {
					cube(size = [6, 6, 5]);
					translate(v = [3.3000000000, 3.3000000000, 0]) {
						cylinder($fn = 12, h = 5.1000000000, r = 1.5000000000);
					}
				}
			}
		}
	}
	translate(v = [3, 38.2000000000, 3]) {
		scale(v = [1, -1, 1]) {
			difference() {
				cube(size = [6, 6, 5]);
				translate(v = [3.3000000000, 3.3000000000, 0]) {
					cylinder($fn = 12, h = 5.1000000000, r = 1.5000000000);
				}
			}
		}
	}
}
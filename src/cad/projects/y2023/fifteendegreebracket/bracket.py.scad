

difference(){
	union() {
		difference() {
			intersection() {
				linear_extrude(height = 15) {
					polygon(points = [[0, 0], [99.1444861374, 13.0526192220], [-99.1444861374, 13.0526192220]]);
				}
				cylinder($fn = 64, h = 15, r = 50);
			}
			translate(v = [0, 107, 2]) {
				cylinder($fn = 64, h = 11, r = 100);
			}
			translate(v = [-14.8716729206, 1.9578928833, 7.5000000000]) {
				rotate(a = -90, v = [-0.9914448614, 0.1305261922, 0.0000000000]) {
					translate(v = [0, 0, -9]) {
						union() {
							cylinder($fn = 16, h = 16, r = 2);
							cylinder($fn = 16, h = 4, r = 4.4000000000);
							translate(v = [0, 0, 3.9990000000]) {
								cylinder($fn = 16, h = 3, r1 = 4.4000000000, r2 = 2);
							}
						}
					}
				}
			}
			translate(v = [-34.7005701481, 4.5684167277, 7.5000000000]) {
				rotate(a = -90, v = [-0.9914448614, 0.1305261922, 0.0000000000]) {
					translate(v = [0, 0, -9]) {
						union() {
							cylinder($fn = 16, h = 16, r = 2);
							cylinder($fn = 16, h = 4, r = 4.4000000000);
							translate(v = [0, 0, 3.9990000000]) {
								cylinder($fn = 16, h = 3, r1 = 4.4000000000, r2 = 2);
							}
						}
					}
				}
			}
			translate(v = [14.8716729206, 1.9578928833, 7.5000000000]) {
				rotate(a = 90, v = [0.9914448614, 0.1305261922, 0.0000000000]) {
					translate(v = [0, 0, -9]) {
						union() {
							cylinder($fn = 16, h = 16, r = 2);
							cylinder($fn = 16, h = 4, r = 4.4000000000);
							translate(v = [0, 0, 3.9990000000]) {
								cylinder($fn = 16, h = 3, r1 = 4.4000000000, r2 = 2);
							}
						}
					}
				}
			}
			translate(v = [34.7005701481, 4.5684167277, 7.5000000000]) {
				rotate(a = 90, v = [0.9914448614, 0.1305261922, 0.0000000000]) {
					translate(v = [0, 0, -9]) {
						union() {
							cylinder($fn = 16, h = 16, r = 2);
							cylinder($fn = 16, h = 4, r = 4.4000000000);
							translate(v = [0, 0, 3.9990000000]) {
								cylinder($fn = 16, h = 3, r1 = 4.4000000000, r2 = 2);
							}
						}
					}
				}
			}
		}
		union() {
			translate(v = [0, 4, 0]) {
				rotate(a = -15, v = [1, 0, 0]) {
					difference() {
						cylinder($fn = 10, h = 15, r = 5);
						translate(v = [-8, -8, -1]) {
							cube(size = [16, 8, 17]);
						}
					}
				}
			}
			translate(v = [0, 4, 15]) {
				scale(v = [1, 1, -1]) {
					rotate(a = -15, v = [1, 0, 0]) {
						difference() {
							cylinder($fn = 10, h = 15, r = 5);
							translate(v = [-8, -8, -1]) {
								cube(size = [16, 8, 17]);
							}
						}
					}
				}
			}
		}
	}
	/* Holes Below*/
	union(){
		union() {
			translate(v = [-100, -100, 15]) {
				cube(size = [200, 200, 15]);
			}
			translate(v = [-100, -100, -15]) {
				cube(size = [200, 200, 15]);
			}
		}
	} /* End Holes */ 
}
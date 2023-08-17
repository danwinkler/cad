

difference(){
	union() {
		cube(size = [67, 46, 4]);
		translate(v = [0, 0, 4]) {
			cube(size = [4, 46, 40]);
		}
		translate(v = [23, 0, 4]) {
			cube(size = [44, 46, 6]);
		}
		translate(v = [0, 0, 4]) {
			cube(size = [67, 4, 40]);
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [41, 4, 0]) {
			rotate(a = -36.8700000000, v = [0, 0, 1]) {
				translate(v = [0, -10, 0]) {
					cube(size = [50, 60, 50]);
				}
			}
		}
		translate(v = [0, 13.5000000000, 24.0000000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
				union() {
					union() {
						translate(v = [0, 0, -5]) {
							cylinder($fn = 12, h = 5, r = 1.9000000000);
						}
						translate(v = [0, 0, -3]) {
							cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
						}
					}
					cylinder($fn = 12, h = 1, r = 4);
				}
			}
		}
		translate(v = [13.5000000000, 0, 18.0000000000]) {
			rotate(a = 90, v = [1, 0, 0]) {
				union() {
					union() {
						translate(v = [0, 0, -5]) {
							cylinder($fn = 12, h = 5, r = 1.9000000000);
						}
						translate(v = [0, 0, -3]) {
							cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
						}
					}
					cylinder($fn = 12, h = 1, r = 4);
				}
			}
		}
	} /* End Holes */ 
}
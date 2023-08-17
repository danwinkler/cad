

difference(){
	union() {
		union() {
			union() {
				cube(size = [115, 70, 2]);
			}
		}
	}
	/* Holes Below*/
	union(){
		union(){
			union(){
				union() {
					union() {
						translate(v = [45.2500000000, 29.8000000000, -1]) {
							cube(size = [24.5000000000, 10.4000000000, 1000]);
						}
						translate(v = [22.7000000000, 35, -0.0010000000]) {
							union() {
								cylinder($fn = 16, h = 2.0020000000, r1 = 2.3000000000, r2 = 3.7500000000);
								translate(v = [0, 0, 2]) {
									cylinder(h = 1000, r = 3.7500000000);
								}
							}
						}
					}
					translate(v = [92.3000000000, 35, -0.0010000000]) {
						union() {
							translate(v = [0, 0, 2]) {
								cylinder(h = 1000, r = 3.7500000000);
							}
							cylinder($fn = 16, h = 2.0020000000, r1 = 2.3000000000, r2 = 3.7500000000);
						}
					}
				}
			}
			union() {
				union() {
					union() {
						union() {
							translate(v = [-1000, -1000, -100]) {
								cube(size = [2000, 2000, 100]);
							}
							translate(v = [-1000, -1000, 0]) {
								cube(size = [1000, 2000, 2]);
							}
						}
						translate(v = [115, -1000, 0]) {
							cube(size = [1000, 2000, 2]);
						}
					}
					translate(v = [0, 70, 0]) {
						cube(size = [1000, 1000, 2]);
					}
				}
				translate(v = [0, -1000, 0]) {
					cube(size = [1000, 1000, 2]);
				}
			}
		}
	} /* End Holes */ 
}
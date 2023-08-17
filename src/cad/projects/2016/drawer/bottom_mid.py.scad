

difference(){
	union() {
		cube(size = [25, 3, 15]);
		translate(v = [0, 8.5000000000, 0]) {
			cube(size = [25, 3, 15]);
		}
		translate(v = [0, 0, 12]) {
			translate(v = [0, 0, 0]) {
				cube(size = [25, 11.5000000000, 3]);
			}
		}
		translate(v = [0, 11.5000000000, 0]) {
			cube(size = [25, 15, 3]);
		}
		translate(v = [12.5000000000, 0, 6.0000000000]) {
			rotate(a = 90, v = [1, 0, 0]) {
			}
		}
		translate(v = [12.5000000000, 19.0000000000, 8]) {
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [12.5000000000, 0, 6.0000000000]){
			rotate(a = 90, v = [1, 0, 0]){
				union() {
					union() {
						translate(v = [0, 0, -12.5000000000]) {
							cylinder($fn = 12, h = 12.5000000000, r = 1.9000000000);
						}
						translate(v = [0, 0, -3]) {
							cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
						}
					}
					cylinder($fn = 12, h = 1, r = 4);
				}
			}
		}
		translate(v = [12.5000000000, 19.0000000000, 8]){
			union() {
				union() {
					translate(v = [0, 0, -9]) {
						cylinder($fn = 12, h = 9, r = 1.9000000000);
					}
					translate(v = [0, 0, -3]) {
						cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
					}
				}
				cylinder($fn = 12, h = 1, r = 4);
			}
		}
	} /* End Holes */ 
}
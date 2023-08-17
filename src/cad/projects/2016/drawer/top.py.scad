

difference(){
	union() {
		cube(size = [3, 31.5000000000, 15]);
		cube(size = [31.5000000000, 3, 15]);
		translate(v = [8.5000000000, 8.5000000000, 0]) {
			cube(size = [3, 23, 15]);
			cube(size = [23, 3, 15]);
		}
		cube(size = [11.5000000000, 31.5000000000, 3]);
		cube(size = [31.5000000000, 11.5000000000, 3]);
		translate(v = [21.5000000000, 0, 9.0000000000]) {
			rotate(a = 90, v = [1, 0, 0]) {
			}
		}
		translate(v = [0, 21.5000000000, 9.0000000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [21.5000000000, 0, 9.0000000000]){
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
		translate(v = [0, 21.5000000000, 9.0000000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
	} /* End Holes */ 
}
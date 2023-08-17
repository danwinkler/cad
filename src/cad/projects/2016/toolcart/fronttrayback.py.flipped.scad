

difference(){
	scale(v = [-1, 1, 1]) {
		union() {
			union() {
				cube(size = [68, 45, 4]);
				cube(size = [27, 59, 4]);
			}
			translate(v = [0, 0, 4]) {
				cube(size = [4, 59, 30]);
			}
			translate(v = [0, 0, 4]) {
				cube(size = [27, 4, 30]);
			}
			translate(v = [23, 0, 4]) {
				cube(size = [4, 22, 30]);
			}
			translate(v = [23, 18, 4]) {
				cube(size = [22.5000000000, 4, 30]);
			}
			translate(v = [23, 41, 4]) {
				cube(size = [4, 18, 30]);
			}
			translate(v = [23, 41, 4]) {
				cube(size = [22.5000000000, 4, 30]);
			}
		}
	}
	/* Holes Below*/
	scale(v = [-1, 1, 1]){
		union(){
			translate(v = [13.5000000000, 0, 19.0000000000]) {
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
			translate(v = [0, 31.5000000000, 19.0000000000]) {
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
		}
	} /* End Holes */ 
}
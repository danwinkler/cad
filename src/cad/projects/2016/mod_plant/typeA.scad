

difference(){
	union() {
		union() {
			union() {
				union() {
					difference() {
						union() {
							cylinder(h = 80, r = 5);
							translate(v = [0, 0, 80]) {
								cylinder($fn = 36, h = 8, r = 2.5000000000);
							}
						}
					}
					translate(v = [0, 0, 5]) {
						rotate(a = 0, v = [0, 0, 1]) {
							rotate(a = 45, v = [0, 1, 0]) {
								union() {
									cylinder(h = 30, r = 5);
									translate(v = [0, 0, 30]) {
										cylinder($fn = 36, h = 8, r = 2.5000000000);
									}
								}
							}
						}
					}
				}
				translate(v = [0, 0, 25]) {
					rotate(a = 180, v = [0, 0, 1]) {
						rotate(a = 45, v = [0, 1, 0]) {
							union() {
								cylinder(h = 30, r = 5);
								translate(v = [0, 0, 30]) {
									cylinder($fn = 36, h = 8, r = 2.5000000000);
								}
							}
						}
					}
				}
			}
			translate(v = [0, 0, 45]) {
				rotate(a = 0, v = [0, 0, 1]) {
					rotate(a = 45, v = [0, 1, 0]) {
						union() {
							cylinder(h = 30, r = 5);
							translate(v = [0, 0, 30]) {
								cylinder($fn = 36, h = 8, r = 2.5000000000);
							}
						}
					}
				}
			}
		}
		translate(v = [0, 0, 65]) {
			rotate(a = 180, v = [0, 0, 1]) {
				rotate(a = 45, v = [0, 1, 0]) {
					union() {
						cylinder(h = 30, r = 5);
						translate(v = [0, 0, 30]) {
							cylinder($fn = 36, h = 8, r = 2.5000000000);
						}
					}
				}
			}
		}
	}
	/* Holes Below*/
	union(){
		union(){
			union(){
				union(){
					difference(){
						cylinder($fn = 36, h = 10, r = 2.7000000000);
					}
				}
			}
		}
	} /* End Holes */ 
}
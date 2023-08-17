

difference(){
	union() {
		translate(v = [0, 0, 0]) {
			cube(size = [27.3000000000, 46.3000000000, 23.3000000000]);
		}
		translate(v = [27.3000000000, 0, 0]) {
			cube(size = [20, 46.3000000000, 4]);
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [0, 0, 0]){
			translate(v = [4, -1, 0]) {
				cube(size = [19.3000000000, 43.3000000000, 28.3000000000]);
			}
			translate(v = [13.6500000000, 46.3000000000, 13.6500000000]) {
				rotate(a = -90, v = [1, 0, 0]) {
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
		translate(v = [0, 15.2790000000, 13.6500000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
				union() {
					union() {
						translate(v = [0, 0, -28.3000000000]) {
							cylinder($fn = 12, h = 28.3000000000, r = 1.9000000000);
						}
						translate(v = [0, 0, -3]) {
							cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
						}
					}
					cylinder($fn = 12, h = 1, r = 4);
				}
			}
		}
		translate(v = [0, 30.5580000000, 13.6500000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
				union() {
					union() {
						translate(v = [0, 0, -28.3000000000]) {
							cylinder($fn = 12, h = 28.3000000000, r = 1.9000000000);
						}
						translate(v = [0, 0, -3]) {
							cylinder($fn = 12, h = 3, r1 = 1.9000000000, r2 = 4);
						}
					}
					cylinder($fn = 12, h = 1, r = 4);
				}
			}
		}
		translate(v = [37.3000000000, 23.1500000000, 0]) {
			rotate(a = 180, v = [0, 1, 0]) {
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
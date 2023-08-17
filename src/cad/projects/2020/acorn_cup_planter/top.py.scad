

difference(){
	union() {
		difference() {
			union() {
				rotate_extrude($fn = 60, angle = 360) {
					projection() {
						union() {
							hull() {
								translate(v = [37.2000000000, 10]) {
									sphere($fn = 16, r = 1.5000000000);
								}
								translate(v = [37.2000000000, 1.5000000000]) {
									sphere($fn = 16, r = 1.5000000000);
								}
							}
							hull() {
								translate(v = [37.2000000000, 1.5000000000]) {
									sphere($fn = 16, r = 1.5000000000);
								}
								translate(v = [30.2000000000, 1.5000000000]) {
									sphere($fn = 16, r = 1.5000000000);
								}
							}
							hull() {
								translate(v = [30.2000000000, 1.5000000000]) {
									sphere($fn = 16, r = 1.5000000000);
								}
								translate(v = [9.0000000000, 42]) {
									sphere($fn = 16, r = 1.5000000000);
								}
							}
						}
					}
				}
				translate(v = [0, 0, 40]) {
					difference() {
						union() {
							sphere($fn = 60, r = 10.5000000000);
						}
						translate(v = [0, 0, -12.0000000000]) {
							sphere($fn = 60, r = 15);
						}
					}
				}
			}
			rotate(a = 0.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
						}
					}
				}
			}
			rotate(a = 60.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
						}
					}
				}
			}
			rotate(a = 120.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
						}
					}
				}
			}
			rotate(a = 180.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
						}
					}
				}
			}
			rotate(a = 240.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
						}
					}
				}
			}
			rotate(a = 300.0000000000, v = [0, 0, 1]) {
				translate(v = [9.0000000000, 0, 0]) {
					hull() {
						cylinder($fn = 16, h = 100, r = 3);
						translate(v = [10.7000000000, 0, 0]) {
							cylinder($fn = 16, h = 100, r = 3);
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
				translate(v = [0, 0, 40]){
					union(){
						union(){
							sphere($fn = 60, r = 7.5000000000);
						}
					}
				}
			}
		}
	} /* End Holes */ 
}
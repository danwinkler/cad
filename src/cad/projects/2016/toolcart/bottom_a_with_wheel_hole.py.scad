

difference(){
	union() {
		cube(size = [60, 27, 46]);
		cube(size = [27, 60, 46]);
		translate(v = [0, 0, 42]) {
			cube(size = [27, 46, 40]);
		}
		translate(v = [13.5000000000, 23.0000000000, 0]) {
			rotate(a = 180, v = [1, 0, 0]) {
			}
		}
		translate(v = [13.5000000000, 34.5000000000, 0]) {
			rotate(a = 180, v = [1, 0, 0]) {
			}
		}
		translate(v = [0, 13.5000000000, 15.1800000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [0, 13.5000000000, 30.3600000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [0, 45.0000000000, 15.1800000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [0, 45.0000000000, 30.3600000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [0, 28.7500000000, 61.1800000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [0, 13.5000000000, 61.1800000000]) {
			rotate(a = -90, v = [0, 1, 0]) {
			}
		}
		translate(v = [30.0000000000, 0, 23.0000000000]) {
			rotate(a = 90, v = [1, 0, 0]) {
			}
		}
		translate(v = [45.0000000000, 0, 23.0000000000]) {
			rotate(a = 90, v = [1, 0, 0]) {
			}
		}
		translate(v = [36.0000000000, 27, 23.0000000000]) {
			rotate(a = -90, v = [1, 0, 0]) {
			}
		}
		translate(v = [48.0000000000, 27, 23.0000000000]) {
			rotate(a = -90, v = [1, 0, 0]) {
			}
		}
		translate(v = [27, 39.0000000000, 23.0000000000]) {
			rotate(a = 90, v = [0, 1, 0]) {
			}
		}
		translate(v = [27, 51.0000000000, 23.0000000000]) {
			rotate(a = 90, v = [0, 1, 0]) {
			}
		}
		translate(v = [13.5000000000, 48.0000000000, -1]) {
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [4, 4, 4]) {
			cube(size = [19, 60, 100]);
			cube(size = [60, 19, 100]);
		}
		translate(v = [4, 4, 56]) {
			cube(size = [50, 50, 50]);
		}
		translate(v = [13.5000000000, 23.0000000000, 0]){
			rotate(a = 180, v = [1, 0, 0]){
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
		translate(v = [13.5000000000, 34.5000000000, 0]){
			rotate(a = 180, v = [1, 0, 0]){
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
		translate(v = [0, 13.5000000000, 15.1800000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [0, 13.5000000000, 30.3600000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [0, 45.0000000000, 15.1800000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [0, 45.0000000000, 30.3600000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [0, 28.7500000000, 61.1800000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [0, 13.5000000000, 61.1800000000]){
			rotate(a = -90, v = [0, 1, 0]){
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
		translate(v = [30.0000000000, 0, 23.0000000000]){
			rotate(a = 90, v = [1, 0, 0]){
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
		translate(v = [45.0000000000, 0, 23.0000000000]){
			rotate(a = 90, v = [1, 0, 0]){
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
		translate(v = [36.0000000000, 27, 23.0000000000]){
			rotate(a = -90, v = [1, 0, 0]){
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
		translate(v = [48.0000000000, 27, 23.0000000000]){
			rotate(a = -90, v = [1, 0, 0]){
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
		translate(v = [27, 39.0000000000, 23.0000000000]){
			rotate(a = 90, v = [0, 1, 0]){
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
		translate(v = [27, 51.0000000000, 23.0000000000]){
			rotate(a = 90, v = [0, 1, 0]){
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
		translate(v = [13.5000000000, 48.0000000000, -1]){
			cylinder($fn = 12, h = 6, r = 3);
		}
	} /* End Holes */ 
}
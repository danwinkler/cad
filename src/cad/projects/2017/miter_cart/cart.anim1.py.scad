

union() {
	scale(v = 25.4000000000) {
		translate(v = [3.0000000000, 3.0000000000, 4]) {
			cube(size = [20.0000000000, 1.5000000000, 3.5000000000]);
			translate(v = [0, 16.5000000000, 0]) {
				cube(size = [20.0000000000, 1.5000000000, 3.5000000000]);
			}
			translate(v = [0, 1.5000000000, 0]) {
				cube(size = [1.5000000000, 15.0000000000, 3.5000000000]);
			}
			translate(v = [18.5000000000, 1.5000000000, 0]) {
				cube(size = [1.5000000000, 15.0000000000, 3.5000000000]);
			}
			translate(v = [0, 0, 3.5000000000]) {
				cube(size = [20.0000000000, 18.0000000000, 0.5000000000]);
			}
		}
		translate(v = [1.5000000000, 1.5000000000, 4]) {
			cube(size = [5.5000000000, 1.5000000000, 32]);
			translate(v = [0, 1.5000000000, 0]) {
				cube(size = [1.5000000000, 3.5000000000, 32]);
			}
			translate(v = [0, 0, -1.5000000000]) {
				cube(size = [5.5000000000, 5.5000000000, 1.5000000000]);
			}
		}
		translate(v = [24.5000000000, 1.5000000000, 4]) {
			scale(v = [-1, 1, 1]) {
				cube(size = [5.5000000000, 1.5000000000, 32]);
				translate(v = [0, 1.5000000000, 0]) {
					cube(size = [1.5000000000, 3.5000000000, 32]);
				}
				translate(v = [0, 0, -1.5000000000]) {
					cube(size = [5.5000000000, 5.5000000000, 1.5000000000]);
				}
			}
		}
		translate(v = [24.5000000000, 22.5000000000, 4]) {
			scale(v = [-1, -1, 1]) {
				cube(size = [5.5000000000, 1.5000000000, 32]);
				translate(v = [0, 1.5000000000, 0]) {
					cube(size = [1.5000000000, 3.5000000000, 32]);
				}
				translate(v = [0, 0, -1.5000000000]) {
					cube(size = [5.5000000000, 5.5000000000, 1.5000000000]);
				}
			}
		}
		translate(v = [1.5000000000, 22.5000000000, 4]) {
			scale(v = [1, -1, 1]) {
				cube(size = [5.5000000000, 1.5000000000, 32]);
				translate(v = [0, 1.5000000000, 0]) {
					cube(size = [1.5000000000, 3.5000000000, 32]);
				}
				translate(v = [0, 0, -1.5000000000]) {
					cube(size = [5.5000000000, 5.5000000000, 1.5000000000]);
				}
			}
		}
		translate(v = [0, 0, 32.5000000000]) {
			cube(size = [26, 1.5000000000, 3.5000000000]);
			translate(v = [0, 22.5000000000, 0]) {
				cube(size = [26, 1.5000000000, 3.5000000000]);
			}
			translate(v = [0, 1.5000000000, 0]) {
				cube(size = [1.5000000000, 21.0000000000, 3.5000000000]);
			}
			translate(v = [24.5000000000, 1.5000000000, 0]) {
				cube(size = [1.5000000000, 21.0000000000, 3.5000000000]);
			}
		}
		translate(v = [0, 0, 36]) {
			cube(size = [26, 24, 0.5000000000]);
		}
		translate(v = [26, 0, 36.5000000000]) {
			rotate(a = 0, v = [0, 1, 0]) {
				cube(size = [24, 0.7500000000, 4.5000000000]);
				translate(v = [0, 23.2500000000, 0]) {
					cube(size = [24, 0.7500000000, 4.5000000000]);
				}
				translate(v = [0, 0.7500000000, 0]) {
					cube(size = [0.7500000000, 22.5000000000, 4.5000000000]);
				}
				translate(v = [23.2500000000, 0.7500000000, 0]) {
					cube(size = [0.7500000000, 22.5000000000, 4.5000000000]);
				}
				translate(v = [0, 0, 4.5000000000]) {
					cube(size = [24, 24, 0.5000000000]);
				}
			}
		}
		translate(v = [0, 0, 36.5000000000]) {
			scale(v = [-1, 1, 1]) {
				rotate(a = $t, v = [0, 1, 0]) {
					cube(size = [24, 0.7500000000, 4.5000000000]);
					translate(v = [0, 23.2500000000, 0]) {
						cube(size = [24, 0.7500000000, 4.5000000000]);
					}
					translate(v = [0, 0.7500000000, 0]) {
						cube(size = [0.7500000000, 22.5000000000, 4.5000000000]);
					}
					translate(v = [23.2500000000, 0.7500000000, 0]) {
						cube(size = [0.7500000000, 22.5000000000, 4.5000000000]);
					}
					translate(v = [0, 0, 4.5000000000]) {
						cube(size = [24, 24, 0.5000000000]);
					}
				}
			}
		}
	}
}
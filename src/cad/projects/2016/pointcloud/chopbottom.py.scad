

union() {
	difference() {
		import(file = "structure.stl", origin = [0, 0]);
		translate(v = [-1000, -1000, -1000]) {
			cube(size = [2000, 2000, 1000]);
		}
	}
}
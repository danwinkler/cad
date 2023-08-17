

union() {
	difference() {
		translate(v = [2, 2, 0]) {
			translate(v = [-10, -10, -10]) {
				import(file = "C:/Users/Dan/workspace/3dprint/dan/project/organic_kumiko/face_conv_surf.py.conv.stl", origin = [0, 0]);
			}
		}
		translate(v = [-10, -10, -10]) {
			difference() {
				cube(size = [200, 200, 200]);
				translate(v = [10, 10, 10]) {
					cube(size = [104, 104, 10]);
				}
			}
		}
	}
}
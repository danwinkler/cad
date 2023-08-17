

difference() {
	difference() {
		difference() {
			cylinder($fn = 36, h = 5.5000000000, r = 10);
			translate(v = [0, 0, -1]) {
				cylinder($fn = 36, h = 3.5000000000, r = 8.5000000000);
			}
		}
		translate(v = [0, 0, 4]) {
			difference() {
				cylinder($fn = 36, h = 3, r = 10.5000000000);
				cylinder($fn = 36, h = 3, r = 8);
			}
		}
	}
	translate(v = [0, 0, 4.5000000000]) {
		linear_extrude(height = 3) {
			text(font = "mana", halign = "center", size = 8, text = "\uE604", valign = "center");
		}
	}
}
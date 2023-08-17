

difference(){
	union() {
		union() {
			cylinder($fn = 60, h = 2, r = 22.2875000000);
			cylinder($fn = 60, h = 76.6125000000, r = 14.2875000000);
			translate(v = [0, 0, 76.6125000000]) {
				sphere($fn = 60, r = 14.2875000000);
			}
		}
	}
	/* Holes Below*/
	union(){
		union(){
			translate(v = [0, 0, -1]) {
				cylinder(h = 77.6125000000, r = 12.2875000000);
			}
			translate(v = [0, 0, 76.6125000000]) {
				sphere($fn = 60, r = 12.2875000000);
			}
		}
	} /* End Holes */ 
}
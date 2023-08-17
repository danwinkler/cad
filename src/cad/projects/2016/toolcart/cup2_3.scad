

difference(){
	union() {
		union() {
			cylinder($fn = 60, h = 2, r = 33.4000000000);
			cylinder($fn = 60, h = 52.8000000000, r = 25.4000000000);
			translate(v = [0, 0, 52.8000000000]) {
				sphere($fn = 60, r = 25.4000000000);
			}
		}
	}
	/* Holes Below*/
	union(){
		union(){
			translate(v = [0, 0, -1]) {
				cylinder(h = 53.8000000000, r = 23.4000000000);
			}
			translate(v = [0, 0, 52.8000000000]) {
				sphere($fn = 60, r = 23.4000000000);
			}
		}
	} /* End Holes */ 
}
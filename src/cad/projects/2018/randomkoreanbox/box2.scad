

difference(){
	union() {
		translate(v = [0, 0, 3]) {
			scale(v = [1, 1, -1]) {
				union() {
					difference() {
						translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
							minkowski() {
								cube(size = [47.0200000000, 67.0200000000, 0.0200000000]);
								rotate(a = 0, v = [1, 0, 0]) {
									sphere($fn = 24, r = 1.4900000000);
								}
							}
						}
						union() {
							translate(v = [0, 0, 3]) {
								scale(v = [1, 1, -1]) {
									union() {
										translate(v = [8.0000000000, 8.0000000000, 3]) {
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
										translate(v = [42.0000000000, 8.0000000000, 3]) {
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
										translate(v = [42.0000000000, 62.0000000000, 3]) {
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
										translate(v = [8.0000000000, 62.0000000000, 3]) {
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
									}
								}
							}
							translate(v = [20, 8, -1]) {
								cube(size = [10, 10, 5]);
							}
						}
					}
					union() {
						translate(v = [0, 0, 3]) {
							scale(v = [1, 1, -1]) {
								union() {
									translate(v = [8.0000000000, 8.0000000000, 3]) {
										difference() {
											cylinder($fn = 24, h = 3.5000000000, r = 3.0000000000);
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
									}
									translate(v = [42.0000000000, 8.0000000000, 3]) {
										difference() {
											cylinder($fn = 24, h = 3.5000000000, r = 3.0000000000);
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
									}
									translate(v = [42.0000000000, 62.0000000000, 3]) {
										difference() {
											cylinder($fn = 24, h = 3.5000000000, r = 3.0000000000);
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
									}
									translate(v = [8.0000000000, 62.0000000000, 3]) {
										difference() {
											cylinder($fn = 24, h = 3.5000000000, r = 3.0000000000);
											translate(v = [0, 0, -2.6000000000]) {
												cylinder($fn = 24, h = 7.1000000000, r = 1.2000000000);
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
		translate(v = [0, 0, 52]) {
			union() {
				difference() {
					translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
						minkowski() {
							cube(size = [47.0200000000, 67.0200000000, 0.0200000000]);
							rotate(a = 0, v = [1, 0, 0]) {
								sphere($fn = 24, r = 1.4900000000);
							}
						}
					}
					union();
				}
				union() {
				}
			}
		}
		translate(v = [0, 3, 0]) {
			rotate(a = 90, v = [1, 0, 0]) {
				union() {
					difference() {
						translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
							minkowski() {
								cube(size = [47.0200000000, 52.0200000000, 0.0200000000]);
								rotate(a = 90, v = [1, 0, 0]) {
									sphere($fn = 24, r = 1.4900000000);
								}
							}
						}
						union() {
							translate(v = [17.5000000000, 13.5000000000, -1]) {
								cube(size = [15, 12, 5]);
							}
						}
					}
					union();
				}
			}
		}
		translate(v = [0, 67, 55]) {
			rotate(a = -90, v = [1, 0, 0]) {
				union() {
					difference() {
						translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
							minkowski() {
								cube(size = [47.0200000000, 52.0200000000, 0.0200000000]);
								rotate(a = 90, v = [1, 0, 0]) {
									sphere($fn = 24, r = 1.4900000000);
								}
							}
						}
						union();
					}
					union();
				}
			}
		}
		translate(v = [3, 0, 0]) {
			rotate(a = -90, v = [0, 1, 0]) {
				union() {
					difference() {
						translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
							minkowski() {
								cube(size = [52.0200000000, 67.0200000000, 0.0200000000]);
								rotate(a = 90, v = [0, 1, 0]) {
									sphere($fn = 24, r = 1.4900000000);
								}
							}
						}
						union();
					}
					union();
				}
			}
		}
		translate(v = [47, 0, 55]) {
			rotate(a = 90, v = [0, 1, 0]) {
				union() {
					difference() {
						translate(v = [1.4900000000, 1.4900000000, 1.4900000000]) {
							minkowski() {
								cube(size = [52.0200000000, 67.0200000000, 0.0200000000]);
								rotate(a = 90, v = [0, 1, 0]) {
									sphere($fn = 24, r = 1.4900000000);
								}
							}
						}
						union();
					}
					union();
				}
			}
		}
	}
	/* Holes Below*/
	union(){
		translate(v = [0, 0, 52]){
			union(){
				union(){
					translate(v = [1.4000000000, 1.4000000000, -0.1000000000]) {
						cube(size = [46.8000000000, 66.8000000000, 3.2000000000]);
					}
				}
			}
		}
	} /* End Holes */ 
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
import boxscad

from solid import *

board_width = 40
board_length = 60

board_margin = 2

box_wall_thickness = 3

box_width = board_width + board_margin*2 + box_wall_thickness*2
box_length = board_length + board_margin*2 + box_wall_thickness*2
box_height = 55

hole_offset = 3
hole_radius = 1.2
standoff_length = 3.5

usb_hole_y_offset = standoff_length + 10
usb_hole_width = 15
usb_hole_height = 12

b = boxscad.RoundedBox(box_width, box_length, box_height, box_wall_thickness)

b.add_ornament(boxscad.Face.TOP, boxscad.ornaments.InsetLid(b.wall_thickness))

b.add_ornament(boxscad.Face.BOTTOM, boxscad.ornaments.StandOffs(
    board_width-(hole_offset*2),
    board_length-(hole_offset*2),
    standoff_length,
    hole_radius,
    wall_hole_depth=b.wall_thickness - .4
))

b.add_ornament(boxscad.Face.BOTTOM, boxscad.ornaments.SquareHole(
    box_wall_thickness+board_margin+15,
    box_wall_thickness+board_margin+3,
    10,
    10
))

b.add_ornament(boxscad.Face.FRONT, boxscad.ornaments.SquareHole(
    (box_width - usb_hole_width) * .5,
    usb_hole_y_offset,
    usb_hole_width,
    usb_hole_height
))

scad_render_to_file(b.render(), 'box2.scad')

boxscad.blueprint.blueprint('blueprint', b)
 
 
************************************************/

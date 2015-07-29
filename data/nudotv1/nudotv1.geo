{
  name:"GEO",
  valid_begin: [0,0],
  valid_end: [0,0],
  gdml_file: "nudotv1.gdml",
  opdet_lv_name: ["volPhotoCathode"],
  opchannel_pv_name: ["pvPMT"],
}

{
  name:"GEO",
  index: "border_tank_wall",
  valid_begin: [0,0],
  valid_end: [0,0],
  mother:"border",
  type:"border",
  volume1:"pvTank",
  volume2:"pvTankAir",
  surface:"stainless_steel",
  reverse:0,
}

{
  name:"GEO",
  index: "border_tank_wall2",
  valid_begin: [0,0],
  valid_end: [0,0],
  mother:"border",
  type:"border",
  volume1:"pvTankAir",
  volume2:"pvTank",
  surface:"stainless_steel",
  reverse:0,
}

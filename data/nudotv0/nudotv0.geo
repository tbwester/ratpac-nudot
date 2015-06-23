{
  name:"GEO",
  valid_begin: [0,0],
  valid_end: [0,0],
  gdml_file: "nudotv0_new.gdml",
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
  volume2:"pvScint",
  surface:"stainless_steel",
  reverse:1,
}
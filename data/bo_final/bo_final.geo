{
  name:"GEO",
  index:"GDML",
  valid_begin: [0,0],
  valid_end: [0,0],
  gdml_file: "bo_final.gdml",
  opdet_lv_name: ["volPhotoCathode"],
  opchannel_pv_name: ["pvPMT"],
}

{
  name:"GEO",
  valid_begin: [0,0],
  valid_end: [0,0],
  mother:"border",
  type:"border",
  volume1:"pvCryo",
  volume2:"pvScint",
  surface:"stainless_steel",
  reverse: 1,
}

{
  name:"GEO",
  valid_begin: [0,0],
  valid_end: [0,0],
  mother:"border",
  type:"border",
  volume1:"pvGlass",
  volume2:"pvScint",
  surface:"glass",
  reverse: 1,
}

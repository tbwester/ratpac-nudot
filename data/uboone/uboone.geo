{
  name:"GEO",
  valid_begin: [0,0],
  valid_end: [0,0],
  gdml_file: "microboone_32pmts_nowires_weldwireplanes.gdml",
  opdet_lv_name: ["vol_PMT_AcrylicPlate","volPaddle_PMT"],
  opchannel_pv_name: ["pvPMT","pvPaddle"]
}

{
  name:"GEO",
  index:"border_tank_wall",
  valid_begin:[0,0],
  valid_end:[0,0],
  mother:"border",
  type:"border",
  volume1:"pvInnerCryostat",	
  volume2:"pvCryostat",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni"
  reverse:0,
}

{
  name:"GEO",
  index:"skin_ground_plate",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volGroundPlate",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_cathode_plate",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volCathodePlate",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_fieldcage_tube_top",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volFieldCageTubeTop",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_fieldcage_tube_bot",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volFieldCageTubeBot",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_fieldcage_tube_front",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volFieldCageTubeFront",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_fieldcage_tube_back",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volFieldCageTubeBack",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}

{
  name:"GEO",
  index:"skin_tpcframe",
  valid_begin:[0,0],
  valid_end:[0,0],	
  mother:"border",
  type:"skin",
  logicalvolume:"volTPCFrame",
  surface:"STEEL_STAINLESS_Fe7Cr2Ni",
}


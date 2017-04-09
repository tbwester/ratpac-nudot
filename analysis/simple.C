// to run
// root
// [0] .L simple.C
// [1] simple("output.root")

int simple( std::string input_file )
{

  // THIS JUST DUMPS THE NUMBER OF PMT hits
  
  RAT::DSReader reader(input_file.c_str());
  
  int nevents = reader.GetTotal();

  for (int iev=0; iev<nevents; iev++) {
    RAT::DS::Root* dsroot = reader.NextEvent();
    RAT::DS::MC* mc = dsroot->GetMC();
    int npes = mc->GetNumPE();
    int npmts = mc->GetMCPMTCount();

    std::cout <<  "Event " << iev << std::endl;
    std::cout << "  nPEs=" << npes << " npmts=" << npmts << std::endl;
  }

  return 0;
};

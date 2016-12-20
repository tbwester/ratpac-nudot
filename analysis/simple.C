int simple()
{

  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  
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

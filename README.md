# rootmagic.py #
This is small jupyter magic to execute ROOT scripts and plot the canvases.
### Setup ###
just copy rootmagic.py into your directory
### Example ###
This will create run.C file and execute it. Canvases c1 and c2 will be saved and printed inside the jupyter notebook

```
#!python

import rootmagic
```

```
#!python

%%rootc -c c1,c2 -f run -i stdio.h
    TCanvas *c1 = new TCanvas("c1","c1",800,600);
    printf("aaaa");
    TH1I *h1 = new TH1I("h1","h1",100,-1,1);
    h1->FillRandom("gaus",10000);
    h1->Draw();
    
    TCanvas *c2 = new TCanvas("c2","c2",800,600);
    TH1I *h2 = new TH1I("h2","h2",100,-1,1);
    h2->FillRandom("gaus",10000);
    h2->Draw();
```
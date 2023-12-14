# %% [markdown]
# Based off of discussion https://github.com/usatlas/analysisbase-dask/issues/4#issuecomment-1831744390
#
# and updated by https://github.com/usatlas/analysisbase-dask/issues/4#issuecomment-1854374286

# %%
import warnings

import awkward as ak
import hist.dask
from coffea.nanoevents import NanoEventsFactory, PHYSLITESchema
from distributed import Client

warnings.filterwarnings("ignore")

# %%
xc = "root://xcache.af.uchicago.edu:1094//"
file_uri = (
    xc
    + "root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/data18_13TeV/df/a4/DAOD_PHYSLITE.34858087._000001.pool.root.1"
)

file_uri_two = (
    xc
    + "root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/data18_13TeV/6c/67/DAOD_PHYSLITE.34858087._000002.pool.root.1"
)

# %%
delayed_hist = hist.dask.Hist.new.Reg(120, 0, 120, label="mass [GeV]").Weight()


# %%
def filter_name(name):
    return name in (
        "AnalysisElectronsAuxDyn.pt",
        "AnalysisElectronsAuxDyn.eta",
        "AnalysisElectronsAuxDyn.phi",
        "AnalysisElectronsAuxDyn.m",
    )


# %%
tree_name = "CollectionTree"
client = Client()

# Question: What is the best way to run over a large collection of files here?
# Write a function?
events = NanoEventsFactory.from_root(
    {file_uri: tree_name, file_uri_two: tree_name},
    schemaclass=PHYSLITESchema,
    permit_dask=True,
    uproot_options=dict(filter_name=filter_name),
).events()

# %%
el_p4 = events.Electrons

# select 2-electron events
evt_filter = ak.num(el_p4) == 2
el_p4 = el_p4[evt_filter]

# fill histogram with di-electron system invariant mass and plot
delayed_hist.fill((el_p4[:, 0] + el_p4[:, 1]).mass / 1_000)
artists = delayed_hist.compute().plot()

# %%
fig = artists[0][0].get_figure()
ax = fig.get_axes()[0]

ax.set_ylabel("Count")
fig.savefig("mass.png")

fig  # Show figure again in notebook

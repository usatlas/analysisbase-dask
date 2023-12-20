# %% [markdown]
# Based off of discussion https://github.com/usatlas/analysisbase-dask/issues/4#issuecomment-1831744390
#
# and updated by https://github.com/usatlas/analysisbase-dask/issues/4#issuecomment-1854374286

# %%
import time
import warnings

import awkward as ak
import hist.dask
from coffea.nanoevents import NanoEventsFactory, PHYSLITESchema
from dask_kubernetes.operator import KubeCluster, make_cluster_spec
from distributed import Client

warnings.filterwarnings("ignore")

# %%
spec = make_cluster_spec(
    name="analysis-base",
    image="hub.opensciencegrid.org/usatlas/analysis-dask-base:latest",
)

cluster = KubeCluster(custom_cluster_spec=spec)

cluster.adapt(minimum=1, maximum=50)  # This doesn't seem to work as expected
print(f"Dashboard: {cluster.dashboard_link}")  # Dashboard link won't open (404s)

# %%
cluster

# %%
client = Client(cluster)

# %%
client

# %%
# xc = "root://xcache.af.uchicago.edu:1094//"
# file_uri = (
#     xc
#     + "root://fax.mwt2.org:1094//pnfs/uchicago.edu/atlaslocalgroupdisk/rucio/data18_13TeV/df/a4/DAOD_PHYSLITE.34858087._000001.pool.root.1"
# )


# %%
# Without filter_name then delayed_hist.compute() will error with
# AttributeError: 'NoneType' object has no attribute 'reset_active_node'
def filter_name(name):
    return name in (
        "AnalysisElectronsAuxDyn.pt",
        "AnalysisElectronsAuxDyn.eta",
        "AnalysisElectronsAuxDyn.phi",
        "AnalysisElectronsAuxDyn.m",
    )


# %%
def get_data_dict(
    n=10,
    read_file="mc.txt",
    tree_name="CollectionTree",
    xc="root://xcache.af.uchicago.edu:1094//",
):
    r = {}
    with open(read_file, "r") as readfile:
        ls = readfile.readlines()
        _range_max = min(n, len(ls))
        print(f"Processing {_range_max} out of {len(ls)} files")
        for i in range(0, _range_max):
            r[xc + ls[i].strip()] = tree_name
    return r


# %%
# file_uris = get_data_dict(10)
file_uris = get_data_dict(100)

events = NanoEventsFactory.from_root(
    file_uris,
    schemaclass=PHYSLITESchema,
    uproot_options=dict(filter_name=filter_name),
    delayed=True,
).events()

# %% [markdown]
# Lay out the event selection logic

# %%
el_p4 = events.Electrons

# select 2-electron events
evt_filter = ak.num(el_p4) == 2
el_p4 = el_p4[evt_filter]

# %% [markdown]
# Then run

# %%
# fill histogram with di-electron system invariant mass and plot
delayed_hist = hist.dask.Hist.new.Reg(120, 0, 120, label="mass [GeV]").Weight()
delayed_hist.fill((el_p4[:, 0] + el_p4[:, 1]).mass / 1_000)

# This takes about 5 minutes for 50 files and 1 worker
_start = time.time()
result_hist = delayed_hist.compute()
_stop = time.time()

print(
    f"Cluster with {cluster.n_workers} workers finished in {_stop-_start:.2f} seconds."
)
delayed_hist.visualize()  # plot the Dask task graph with graphviz

artists = result_hist.plot()

# %% [markdown]
# Now scale across the KubeCluster to multiple workers

# %%
cluster.scale(50)
cluster

# %%
# fill histogram with di-electron system invariant mass and plot
delayed_hist = hist.dask.Hist.new.Reg(120, 0, 120, label="mass [GeV]").Weight()
delayed_hist.fill((el_p4[:, 0] + el_p4[:, 1]).mass / 1_000)

# This takes about:
# 24 seconds for 50 files and 10 workers
# 13 seconds for 50 files and 25 workers
# 11 seconds for 50 files and 50 workers
# 12 seconds for 50 files and 100 workers
_start = time.time()
result_hist = delayed_hist.compute()
_stop = time.time()

print(
    f"Cluster with {cluster.n_workers} workers finished in {_stop-_start:.2f} seconds."
)
delayed_hist.visualize()

artists = result_hist.plot()

# %%
fig = artists[0][0].get_figure()
ax = fig.get_axes()[0]

ax.set_ylabel("Count")
fig.savefig("mass.png")

fig  # Show figure again in notebook

# %%
client.close()
cluster.close()

import xarray as xr
import numpy as np
from .steric import steric, thermosteric, halosteric
from .eos.wright import wright

np.random.seed(123)
time = xr.DataArray([1.0, 2.0, 3.0, 4.0, 5.0], dims=("time"))
z_l = xr.DataArray(np.array([2.5, 50.0, 100.0, 1000.0, 5000.0]), dims=("z_l"))
xh = xr.DataArray([1.0, 2.0, 3.0, 4.0, 5.0], dims="xh")
yh = xr.DataArray([1.0, 2.0, 3.0, 4.0, 5.0], dims="yh")

thetao = xr.DataArray(
    np.random.normal(15.0, 5.0, (5, 5, 5, 5)),
    dims=({"time": time, "z_l": z_l, "yh": yh, "xh": xh}),
)
so = xr.DataArray(
    np.random.normal(35.0, 1.5, (5, 5, 5, 5)),
    dims=({"time": time, "z_l": z_l, "yh": yh, "xh": xh}),
)
volcello = xr.DataArray(
    np.random.normal(1000.0, 100.0, (5, 5, 5, 5)),
    dims=({"time": time, "z_l": z_l, "yh": yh, "xh": xh}),
)
areacello = xr.DataArray(
    np.random.normal(100.0, 10.0, (5, 5)), dims=({"yh": yh, "xh": xh})
)

dset = xr.Dataset(
    {"thetao": thetao, "so": so, "volcello": volcello, "areacello": areacello}
)
dset = dset.assign_coords({"time": time, "z_l": z_l, "yh": yh, "xh": xh})


def test_steric_broadcast():
    result = steric(dset)
    reference = float(result["reference_rho"][1, 2, 3])
    rho = wright(
        float(dset["thetao"][0, 1, 2, 3]),
        float(dset["so"][0, 1, 2, 3]),
        float(dset["z_l"][1]) * 1.0e4,
    )
    assert np.allclose(reference, rho)


def test_halosteric_values():
    result = halosteric(dset).sum()
    assert np.allclose(result["reference_so"], 4386.684378216)
    assert np.allclose(result["reference_vol"], 125401.862523944)
    assert np.allclose(result["reference_rho"], 128880.6037745114)
    assert np.allclose(result["reference_height"], 1230.16465627079)
    assert np.allclose(result["expansion_coeff"], 0.079859382545713)
    assert np.allclose(result["halosteric"], 0.7438560821420365)


def test_steric_values():
    result = steric(dset).sum()
    assert np.allclose(result["reference_so"], 4386.684378216)
    assert np.allclose(result["reference_vol"], 125401.862523944)
    assert np.allclose(result["reference_rho"], 128880.6037745114)
    assert np.allclose(result["reference_height"], 1230.16465627079)
    assert np.allclose(result["expansion_coeff"], 0.0321479462294750)
    assert np.allclose(result["steric"], 0.2186699101982375)


def test_thermosteric_values():
    result = thermosteric(dset).sum()
    assert np.allclose(result["reference_so"], 4386.684378216)
    assert np.allclose(result["reference_vol"], 125401.862523944)
    assert np.allclose(result["reference_rho"], 128880.6037745114)
    assert np.allclose(result["reference_height"], 1230.16465627079)
    assert np.allclose(result["expansion_coeff"], -0.0485257018113030)
    assert np.allclose(result["thermosteric"], -0.533707251686609)


def test_halosteric_global_values():
    result = halosteric(dset, domain="global").sum()
    assert np.allclose(result["reference_thetao"], 1892.9343653921171)
    assert np.allclose(result["reference_so"], 4386.6843782162)
    assert np.allclose(result["reference_vol"], 125401.8625239444)
    assert np.allclose(result["reference_rho"], 128880.60377451136)
    assert np.allclose(result["reference_height"], 6109.02357321457)
    assert np.allclose(result["expansion_coeff"], 0.07137665705082741)
    assert np.allclose(result["global_reference_vol"], 125401.8625239444)
    assert np.allclose(result["global_reference_rho"], 1030.9696145532507)
    assert np.allclose(result["halosteric"], 0.027906667552048414)


def test_steric_global_values():
    result = steric(dset, domain="global").sum()
    assert np.allclose(result["reference_thetao"], 1892.9343653921171)
    assert np.allclose(result["reference_so"], 4386.6843782162)
    assert np.allclose(result["reference_vol"], 125401.8625239444)
    assert np.allclose(result["reference_rho"], 128880.60377451136)
    assert np.allclose(result["reference_height"], 6109.02357321457)
    assert np.allclose(result["expansion_coeff"], 0.022642849677982482)
    assert np.allclose(result["global_reference_vol"], 125401.8625239444)
    assert np.allclose(result["global_reference_rho"], 1030.9696145532507)
    assert np.allclose(result["steric"], 0.008852844956643128)


def test_thermosteric_global_values():
    result = thermosteric(dset, domain="global").sum()
    assert np.allclose(result["reference_thetao"], 1892.9343653921171)
    assert np.allclose(result["reference_so"], 4386.6843782162)
    assert np.allclose(result["reference_vol"], 125401.8625239444)
    assert np.allclose(result["reference_rho"], 128880.60377451136)
    assert np.allclose(result["reference_height"], 6109.02357321457)
    assert np.allclose(result["expansion_coeff"], -0.049692744362344)
    assert np.allclose(result["global_reference_vol"], 125401.8625239444)
    assert np.allclose(result["global_reference_rho"], 1030.9696145532507)
    assert np.allclose(result["thermosteric"], -0.019428745390546228)
import pytest
import numpy as np

from momlevel import steric, thermosteric, halosteric
from momlevel.eos import wright
from momlevel.test_data import generate_test_data

dset = generate_test_data()


def test_steric_broadcast():
    result, reference = steric(dset)
    reference = float(reference["rho"][1, 2, 3])
    rho = wright(
        float(dset["thetao"][0, 1, 2, 3]),
        float(dset["so"][0, 1, 2, 3]),
        float(dset["z_l"][1]) * 1.0e4,
    )
    assert np.allclose(reference, rho)


def test_steric_incorrect_area():
    dset2 = dset.copy()
    dset2["areacello"] = dset2["areacello"] * 1.3
    with pytest.raises(Exception):
        _ = steric(dset2)


reference_results = {
    "reference_thetao": 1892.9343653921171,
    "reference_so": 4386.6843782162,
    "reference_vol": 125401.8625239444,
    "reference_rho": 128880.60377451136,
    "reference_height": 8.74107451e-09,
    "global_reference_height": 4.340836e-08,
    "global_reference_vol": 125401.8625239444,
    "global_reference_rho": 1030.9696145532507,
}


def test_halosteric_values():
    result, reference = halosteric(dset)
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["reference_height"]
    )
    assert np.allclose(result["expansion_coeff"], 0.079859382545713)
    assert np.allclose(result["halosteric"], 5.28555377e-12)


def test_steric_values():
    result, reference = steric(dset)
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["reference_height"]
    )
    assert np.allclose(result["expansion_coeff"], 0.0321479462294750)
    assert np.allclose(result["steric"], 1.55378385e-12)


def test_thermosteric_values():
    result, reference = thermosteric(dset)
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["reference_height"]
    )
    assert np.allclose(result["expansion_coeff"], -0.0485257018113030)
    assert np.allclose(result["thermosteric"], -3.79231742e-12)


def test_halosteric_global_values():
    result, reference = halosteric(dset, domain="global")
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["global_reference_height"]
    )
    assert np.allclose(reference["volo"], reference_results["global_reference_vol"])
    assert np.allclose(reference["rhoga"], reference_results["global_reference_rho"])
    assert np.allclose(result["expansion_coeff"], 0.07137665705082741)
    assert np.allclose(result["halosteric"], 1.98293992e-13)


def test_steric_global_values():
    result, reference = steric(dset, domain="global")
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["global_reference_height"]
    )
    assert np.allclose(reference["volo"], reference_results["global_reference_vol"])
    assert np.allclose(reference["rhoga"], reference_results["global_reference_rho"])
    assert np.allclose(result["expansion_coeff"], 0.022642849677982482)
    assert np.allclose(result["steric"], 6.29048941e-14)


def test_thermosteric_global_values():
    result, reference = thermosteric(dset, domain="global")
    result = result.sum()
    reference = reference.sum()
    assert np.allclose(reference["thetao"], reference_results["reference_thetao"])
    assert np.allclose(reference["so"], reference_results["reference_so"])
    assert np.allclose(reference["volcello"], reference_results["reference_vol"])
    assert np.allclose(reference["rho"], reference_results["reference_rho"])
    assert np.allclose(
        result["reference_height"], reference_results["global_reference_height"]
    )
    assert np.allclose(reference["volo"], reference_results["global_reference_vol"])
    assert np.allclose(reference["rhoga"], reference_results["global_reference_rho"])
    assert np.allclose(result["expansion_coeff"], -0.049692744362344)
    assert np.allclose(result["thermosteric"], -1.38053154e-13)
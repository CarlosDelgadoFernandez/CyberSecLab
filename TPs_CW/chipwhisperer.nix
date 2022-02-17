{ lib
, fetchPypi
, buildPythonPackage
, pythonOlder
, tqdm
, pyserial
, cython
, ecpy
, pyusb
, numpy
, scipy
, fastdtw
, configobj
}:

buildPythonPackage rec {
  pname = "chipwhisperer";
  version = "5.5.2";

  disabled = pythonOlder "3.6";

  src = fetchPypi {
    inherit pname version;
    sha256 = "sha256-amUzHZ2EWCrKRm4FowPUrxYhcI3ifLn3bxAo/T7SXoQ=";
  };

  propagatedBuildInputs = [
    tqdm
    pyserial
    cython
    ecpy
    pyusb
    numpy
    scipy
    fastdtw
    configobj
  ];

  doCheck = false;

  pythonImportsCheck = [ "chipwhisperer" ];

  meta = with lib; {
    description = "ChipWhisperer Side-Channel Analysis Tool";
    homepage = "https://github.com/newaetech/chipwhisperer";
    license = licenses.gpl3;
  };
}
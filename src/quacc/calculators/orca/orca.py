"""A ORCA6 based ASE-calculator"""

from __future__ import annotations

from msilib.schema import Class
from typing import TYPE_CHECKING

from ase.calculators.calculator import FileIOCalculator

from quacc.calculators.orca.io import read_orca, write_orca


if TYPE_CHECKING:
    from typing import Any, Optional, ClassVar, Literal

    from ase.atoms import Atoms

    from quacc.types import OrcaResults

class Orca(FileIOCalculator):
    """
    A ORCA6 ASE calculator built around Custodian.

    """

    implemented_properties: ClassVar[list[str]] = ["Geometry", "SCF_Energy", "DFT_Energy", "Solvation_Details", "Loewdin_Population_Analysis", "VdW_Correction", "SCF_Nuc_Gradient", "SCF_Dipole_Moment"]

    results: ClassVar[OrcaResults] = {}

    def __init__(
        self,
        atoms: [Atoms, str] | None = "inp.xyz",
        input_settings: dict | None = {"functional": "wb97x-d3bj", "basis": "def2-tzvp",},
        charge: int = 0,
        spin_multiplicity: int = 1,
        solvation: dict | None = None,
        write_property_json: bool = True,
        **fileiocalculator_kwargs,
    ) -> None:
        """Initialize the Orca calculator.

        Args:
            atoms (Atoms, str] | None, optional): Input geometry. Filename of .xyz file or ASE Atoms object.
            charge (int, optional): Charge of the system. Defaults to 0.
            spin_multiplicity (int, optional): Multiplicity of the system. Defaults to 1.
            input_settings (dict | None, optional): Dictionary of input settings. Values of keys will be passed to the input file. 
            solvation (dict | None, optional): Dictionary of solvation settings. Key-value pairs will be printed in cpcm block.
            write_property_json (bool, optional): Write the properties to a json file. Defaults to True.
            **fileiocalculator_kwargs: Keyword arguments to be passed to FileIOCalculator.
        """
       # assign variables to self
        self.atoms = atoms
        self.input_settings = input_settings
        self.charge = charge
        self.spin_multiplicity = spin_multiplicity
        self.solvation = solvation
        self.write_property_json = write_property_json



        FileIOCalculator.__init__(self, restart=None, ignore_bad_restart_file=True)

    def write_input(self, atoms: Atoms, properties: dict[str, Any]) -> None:
        """Write the input file for ORCA.

        Args:
            atoms (Atoms): ASE Atoms object.
            properties (dict[str, Any]): Dictionary of properties to be calculated.
        """
        write_orca(atoms, self.label, self.scratch, self.command)

    def read_results(self) -> OrcaResults:
        return read_orca(self.label)

    def calculate(self, atoms: At
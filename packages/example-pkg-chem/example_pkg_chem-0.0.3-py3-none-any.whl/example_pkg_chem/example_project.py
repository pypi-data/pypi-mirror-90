"""
Example project

@author: dajt mullaj
"""

from rdkit import Chem
from rdkit.Chem import Draw
import example_pkg_20175707

class DrawMol:
    def fromSmiles(smiles):
        template = Chem.MolFromSmiles(smiles)
        Draw.MolToFile(template,'{}.png'.format(smiles)) 

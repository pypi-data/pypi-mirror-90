from more_itertools import collapse
from pkg_resources import get_distribution
from typing import Collection, TYPE_CHECKING, List, Dict, Tuple, Set, Deque

from .linear import LinearFingerprint


cgr_version = get_distribution('CGRtools').parsed_version
if cgr_version.major == 4 and cgr_version.minor == 0:  # 4.0 compatibility
    from CGRtools.algorithms.morgan import tuple_hash
else:
    from CGRtools._functions import tuple_hash

if TYPE_CHECKING:
    from CGRtools import MoleculeContainer


class MorganFingerprint(LinearFingerprint):
    def __init__(self):
        super().__init__()

    def _morgan(self, molecule: 'MoleculeContainer'):
        bonds = molecule._bonds

        identifiers = {idx: tuple_hash((atom.neighbors, atom.hybridization, atom.atomic_number,
                                        atom.atomic_mass, atom.charge, atom.total_hydrogens,
                                        *sorted(bonds[idx].values(),
                                                key=lambda x: x.order,
                                                reverse=True)))
                       for idx, atom in molecule.atoms()}
        arr = set()

        for step in range(1, self._max_radius + 1):
            if step == 1 and self._min_radius <= 1:
                arr |= set(identifiers.values())
            elif step == 1:
                continue
            identifiers = {idx: tuple_hash((tpl, *collapse(sorted((x[::-1] for x in bonds[idx].items()),
                                                                  key=lambda x: int(x[1]),
                                                                  reverse=True))))
                           for idx, tpl in identifiers.items()}

            if step >= self._min_radius:
                arr |= set(identifiers.values())

        return arr

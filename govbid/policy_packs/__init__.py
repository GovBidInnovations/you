"""Policy pack interface for the GovBid engine.

Policy packs encapsulate the prime directive version, dossier template
version and coverage bundle version expected by a given set of rules.
"""

from .loader import load_policy_pack, PolicyPack  # noqa: F401

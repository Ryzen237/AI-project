from core.gauge_theory import GaugeField

def test_gauge_initialization():
    gf = GaugeField()
    assert len(gf.A_mu) == 4
    print("Test réussi!")
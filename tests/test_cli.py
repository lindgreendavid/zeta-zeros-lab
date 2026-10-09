from zeta_zeros_lab.cli import main


def test_cli_prints_both_blocks(capsys):
    main()
    out = capsys.readouterr().out
    assert "low:" in out and "high:" in out
    assert "ks_gue=" in out

from __future__ import annotations

import tkinter as tk

import pytest
from PIL import Image

from app import SteganographyApp
from metrics import evaluate_quality


def test_quality_evaluation_includes_ssim(tmp_path):
    original = tmp_path / "original.png"
    stego = tmp_path / "stego.png"
    Image.new("RGB", (32, 32), (10, 20, 30)).save(original)
    Image.new("RGB", (32, 32), (10, 20, 31)).save(stego)

    result = evaluate_quality(original, stego)

    assert 0.0 <= result["ssim"] <= 1.0


def test_gui_constructs_and_password_state_tracks_method():
    try:
        root = tk.Tk()
    except tk.TclError as exc:
        pytest.skip(f"Tk display unavailable: {exc}")
    root.withdraw()
    try:
        app = SteganographyApp(root)
        root.update_idletasks()
        assert len(app.notebook.tabs()) == 4
        assert str(app.encode_key_entry.cget("state")) == "disabled"

        app.encode_method_var.set("random")
        root.update_idletasks()
        assert str(app.encode_key_entry.cget("state")) == "normal"

        app.encode_method_var.set("basic")
        app.aes_var.set(True)
        app._update_encode_password_state()
        assert str(app.encode_key_entry.cget("state")) == "normal"
    finally:
        root.destroy()

from rea_video.i18n import LangDict, T, join, set_lang
from rea_video.classify import LABEL_ZH


def test_T_and_langdict_follow_language():
    try:
        set_lang("zh")
        assert T("实拍", "live action") == "实拍"
        assert LABEL_ZH["ai_video"] == "AI 生成视频"
        assert join(["a", "b"]) == "a、b"
        set_lang("en")
        assert T("实拍", "live action") == "live action"
        assert T("{n} 个镜头", "{n} shots", n=3) == "3 shots"
        assert T("只有中文") == "只有中文"  # no English yet: falls back
        assert LABEL_ZH["ai_video"] == "AI-generated video"
        assert dict(LABEL_ZH.items())["cg_3d"] == "3D render"
        assert join(["a", "b"]) == "a, b"
        d = LangDict({"x": "甲"}, en={})
        assert d["x"] == "甲" and "x" in d and len(d) == 1
    finally:
        set_lang("zh")


def test_unknown_language_rejected():
    import pytest

    with pytest.raises(ValueError):
        set_lang("fr")


def test_japanese_uses_catalogue_then_english():
    try:
        set_lang("ja")
        assert T("实拍", "live action") == "実写"
        assert LABEL_ZH["ai_video"] == "AI 生成動画"
        assert T("{n} 个音效", "{n} effects", n=3) == "効果音 3 個"
        assert T("目录里没有的句子", "not in the catalogue") == "not in the catalogue"
        assert T("只有中文") == "只有中文"
        assert join(["a", "b"]) == "a、b"
    finally:
        set_lang("zh")


def test_japanese_catalogue_keeps_placeholders():
    from string import Formatter

    from rea_video.locale_ja import JA

    def fields(s):
        return sorted((f, spec) for _, f, spec, _ in Formatter().parse(s) if f is not None)

    assert not [zh for zh, ja in JA.items() if fields(zh) != fields(ja)]

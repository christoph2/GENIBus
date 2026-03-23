from genibus.utils import classes


class SingletonKlass(classes.SingletonBase):
    pass


class DemoRepresentation(classes.RepresentationMixIn):
    def __init__(self) -> None:
        self.number = 16
        self.value = 2.5
        self.missing = None
        self.payload = bytearray([0x01, 0x02])
        self.name = "demo"


def test_singleton_identity() -> None:
    inst0 = SingletonKlass()
    inst1 = SingletonKlass()

    assert id(inst0) == id(inst1)


def test_representation_mixin_python3_safe() -> None:
    rendered = repr(DemoRepresentation())

    assert "DemoRepresentation {" in rendered
    assert "number = 0x10" in rendered
    assert "value = 2.5" in rendered
    assert "missing = None" in rendered
    assert "payload = 0x01, 0x02" in rendered
    assert "name = 'demo'" in rendered
    assert rendered.endswith("}")


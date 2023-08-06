"""Message Defintions."""
import collections
import copy

from anytree import NodeMixin

from .util import repr_

_MsgDef = collections.namedtuple("_MsgDef", "circuit name read prio write update")


class MsgDef(_MsgDef, NodeMixin):

    """
    Message Definition.

    Args:
        circuit (str): Circuit Name
        name (str): Message Name
        children (tuple): Fields

    Keyword Args:
        read (bool): Message intend to be read
        prio (int): Message Polling Priority
        write (bool): Message intend to be written
        updated (bool): Message intent to be seen automatically on every value change
    """

    __slots__ = tuple()

    def __new__(cls, circuit, name, children, read=False, prio=None, write=False, update=False):
        if not read:
            prio = None
        msgdef = _MsgDef.__new__(cls, circuit, name, read, prio, write, update)
        if children:
            msgdef.children = children
        return msgdef

    def __repr__(self):
        args = (self.circuit, self.name, self.children)
        kwargs = [
            ("read", self.read, False),
            ("prio", self.prio, None),
            ("write", self.write, False),
            ("update", self.update, False),
        ]
        return repr_(self, args, kwargs)

    def __hash__(self):
        return hash((self.circuit, self.name, self.children, self.read, self.prio, self.write, self.update))

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return (self.circuit, self.name, self.children, self.read, self.prio, self.write, self.update) == (
                other.circuit,
                other.name,
                other.children,
                other.read,
                other.prio,
                other.write,
                other.update,
            )
        else:
            return NotImplemented

    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return not self == other
        else:
            return NotImplemented

    @property
    def fields(self):
        """Fields."""
        return tuple(child for child in self.children if isinstance(child, FieldDef))

    @property
    def virtfields(self):
        """Generic Fields."""
        return tuple(child for child in self.children if isinstance(child, VirtFieldDef))

    @property
    def ident(self):
        """Identifier."""
        return f"{self.circuit}/{self.name}"

    @property
    def type_(self):
        """Message Type."""
        read = "r" if self.read else "-"
        prio = f"{self.prio}" if self.prio else "-"
        write = "w" if self.write else "-"
        update = "u" if self.update else "-"
        return "".join((read, prio, write, update))

    def join(self, msgdef):
        """Return Joined Message Definition."""
        if (self.circuit, self.name, self.children) == (msgdef.circuit, msgdef.name, msgdef.children):
            return MsgDef(
                self.circuit,
                self.name,
                tuple(copy.copy(fielddef) for fielddef in self.children),
                read=self.read or msgdef.read,
                prio=self.prio or msgdef.prio,
                write=self.write or msgdef.write,
                update=self.update or msgdef.update,
            )
        else:
            return None


_FieldDef = collections.namedtuple("_FieldDef", "idx name type_ unit comment")


class AbstractFieldDef(_FieldDef, NodeMixin):

    """
    Abstract Field Definition.

    Args:
        idx (str): Index within Message
        name (str): Unique name (as `name` may be used multiple times by ebus)
        type_ (Type): Type

    Keywords Args:
        unit (str): Unit of the field value
        comment (str): Comment.
    """

    __slots__ = tuple()

    def __new__(cls, idx, name, type_, unit=None, comment=None):
        return _FieldDef.__new__(cls, idx, name, type_, unit or None, comment or None)

    def __repr__(self):
        args = (self.idx, self.name, self.type_)
        kwargs = [
            ("unit", self.unit, None),
            ("comment", self.comment, None),
        ]
        return repr_(self, args, kwargs)

    def _pre_detach(self, parent):
        # it is forbidden to remove fields from their message - create new one
        assert False, f"{self!r} is already used by {parent!r}"  # pragma: no cover

    @property
    def msgdef(self):
        """Message Definition."""
        return self.parent

    @property
    def ident(self):
        """Identifier."""
        return f"{self.parent.ident}/{self.name}" if self.parent else None

    def __copy__(self):
        return FieldDef(idx=self.idx, name=self.name, type_=self.type_, unit=self.unit)


class FieldDef(AbstractFieldDef):

    """
    Field Definition.

    Args:
        idx (str): Index within Message
        name (str): Unique name (as `name` may be used multiple times by ebus)
        type_ (Type): Type

    Keywords Args:
        unit (str): Unit of the field value
        comment (str): Comment.
    """


class VirtFieldDef(AbstractFieldDef):
    """
    Virtual Field Definition.

    Args:
        name (str): Unique name (as `name` may be used multiple times by ebus)
        type_ (Type): Type
        func: Function to create value.

    Keywords Args:
        unit (str): Unit of the field value
        comment (str): Comment.
    """

    def __new__(cls, name, type_, func, unit=None, comment=None):
        obj = AbstractFieldDef.__new__(cls, None, name, type_, unit or None, comment or None)
        obj.func = func
        return obj

    def __repr__(self):
        return repr_(self, (self.name, self.type_))

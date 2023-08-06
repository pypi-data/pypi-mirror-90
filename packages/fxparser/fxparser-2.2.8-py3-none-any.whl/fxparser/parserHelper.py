from .actionParser import ActionParser
from .priceParser import PriceParser
from .slParser import SLParser
from .tpParser import TPParser
from .urgencyParser import UrgencyParser
from .symbolParser import SymbolParser
import dataclasses as dc

@dc.dataclass(unsafe_hash=True)
class ForexDTO():
    symbol: str = ""
    price: float = 0.0
    market: bool = True
    sl: float = 0.0
    tp: float = 0.0
    tp2: float = 0.0
    tp3: float = 0.0
    tp4: float = 0.0
    tp5: float = 0.0
    lotSize: float = 0.07
    type: int = 0

class ParserHelper():
    def __init__(self):
        self.actionParser = ActionParser()
        self.priceParser = PriceParser()
        self.slParser = SLParser()
        self.tpParser = TPParser()
        self.urgencyParser = UrgencyParser()
        self.symbolParser = SymbolParser()

    def parse_text(self, text):
        result = ForexDTO()
        text = self.actionParser.clean_text(text)
        action = self.actionParser.parse_text(text)
        sl = self.slParser.parse_text(text)
        tp = self.tpParser.parse_text(text)
        urgency = self.urgencyParser.parse_text(text)
        price = self.priceParser.parse_text(text, tp, sl)
        symbol = self.symbolParser.parse_text(text)

        result.type = 1 if action == "BUY" else 2
        result.sl = float(sl) if sl else 0.0
        result.tp = float(tp[0]) if len(tp) > 0 else 0.0
        result.tp2 = float(tp[1]) if len(tp) > 1 else 0.0
        result.tp3 = float(tp[2]) if len(tp) > 2 else 0.0
        result.tp4 = float(tp[3]) if len(tp) > 3 else 0.0
        result.tp5 = float(tp[4]) if len(tp) > 4 else 0.0
        result.market = urgency
        result.price = float(price) if price else 0.0
        result.symbol = symbol

        return result

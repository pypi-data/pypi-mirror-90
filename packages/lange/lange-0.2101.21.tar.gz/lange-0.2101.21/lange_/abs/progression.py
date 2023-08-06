import decimal as dec
import math

from lange_.tricks import detect_precision


class Progression:
    def __init__(self, op, null, prod_f, div_f, pow_f, bins_f, args, maxdigits=28):
        self.prod_f, self.div_f, self.pow_f = prod_f, div_f, pow_f
        self.op = op
        self.decctx = dec.Context()
        null = self.decctx.create_decimal(null)
        if Ellipsis in args:
            if not (3 <= len(args) <= 4) or args[2] is not Ellipsis:
                raise Exception("Among 3 or 4 arguments, '...' should be the third.")

            # Detect level of precision and enforce it for the rest of this object life.
            end = 0 if len(args) == 3 else args[-1]
            self.precision = max(
                detect_precision(args[0], maxdigits),
                detect_precision(args[1], maxdigits),
                detect_precision(end, maxdigits)
            )
            self.decctx.prec = self.precision

            # Protect all provided numbers from floating point inequality issues (e.g. 0.8 - 0.6 != 0.2).
            self.start = self.decctx.create_decimal(args[0])
            self.second = self.decctx.create_decimal(args[1])
            self.end = self.decctx.create_decimal(math.inf if len(args) == 3 else args[-1])

            # Derived attributes.
            self.step = div_f(self.second, self.start)
            self.cast = int if all(isinstance(v, int) for v in args[:2]) and int(self.step) == self.step else float
            bins = bins_f(self.start, self.end, self.step).to_integral_exact(rounding=dec.ROUND_FLOOR)
            self.size = bins + self.decctx.create_decimal(1)

            def g():
                s, i = self.start, 0
                while i < self.size:
                    yield self.cast(s)
                    s = prod_f(s, self.step)
                    i += 1

            self.gen = g
        elif len(args) == 0:
            self.start, self.step, self.end = None, None, None
            self.size = 0
            self.gen = lambda: iter(())
            self.cast = lambda x: x
        elif 1 <= len(args) <= 2:
            self.start = self.decctx.create_decimal(args[0])
            self.step = null if len(args) == 1 else self.div_f(self.decctx.create_decimal(args[1]), self.start)
            self.end = self.decctx.create_decimal(args[-1])
            self.size = len(args)
            self.gen = lambda: iter(args)
            self.cast = int if all(isinstance(v, int) for v in args) and int(self.step) == self.step else float
        else:
            self.start, self.step, self.end = None, None, None
            self.size = len(args)
            self.gen = lambda: iter(args)
            self.cast = int if all(isinstance(v, int) for v in args) else float

    def __iter__(self):
        return self.gen()

    def __getitem__(self, item):
        if isinstance(item, slice):
            if self.start is None:
                return self.__class__(*list(self)[item])
            item_start = item.start or self.decctx.create_decimal(0)
            item_step = item.step or self.decctx.create_decimal(1)
            start = self.decctx.create_decimal(self[item_start])
            step = self.div_f(self.decctx.create_decimal(self[item_start + item_step]), start)
            second = self.prod_f(start, step)
            end = self.prod_f(start, self.pow_f(step, (item.stop - item_start - 1) // item_step))
            args = start, second, ..., end
            return self.__class__(*args)  # REMINDER: calling child class.

        if self.start is None:
            return self.__class__(list(self)[item])

        if not (0 <= item < self.size):
            raise Exception(f"Index {item} outside valid range [0; {self.size}[.")
        return self.cast(self.prod_f(self.start, self.pow_f(self.step, item)))

    def __str__(self):
        return f"[{' '.join(map(str, self))}]"

    def __repr__(self):
        if self.start is None:
            return str(self)
        end = self.cast(self.end)
        return f"[{self.cast(self.start)} {self.cast(self.prod_f(self.start, self.step))} .{self.op}. {end}]"

    def __invert__(self):
        return list(self)

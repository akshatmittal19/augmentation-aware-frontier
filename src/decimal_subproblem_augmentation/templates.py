"""Built-in wording bank and placeholder contract for decimal subproblems."""

FAMILY_FIELDS = {
    "additive_balance": {"total", "known", "variable"},
    "subtraction_remainder": {"initial", "removed", "variable"},
    "equal_shares": {"total", "count", "variable"},
    "unit_price": {"count", "total", "variable"},
    "rectangle_area": {"area", "width", "variable"},
    "rectangle_perimeter": {"perimeter", "width", "variable"},
    "constant_rate": {"distance", "hours", "variable"},
    "missing_average": {"known", "mean", "variable"},
    "midpoint": {"endpoint", "midpoint", "variable"},
    "map_scale": {"scale", "actual", "variable"},
    "arithmetic_sequence": {"first", "index", "last", "variable"},
    "equal_edge_path": {"edges", "total", "variable"},
    "percentage": {"percent", "total", "variable"},
    "place_value": {"integer", "places", "variable"},
    "quotient": {"numerator", "denominator", "variable"},
}


BUILTIN_FAMILY_TEMPLATES = {
    "additive_balance": [
        "Two containers hold {total} liters altogether. One holds {known} liters. "
        "The other holds {variable} liters. Find {variable}.",
        "A total of {total} units is split into portions of {known} and {variable}. "
        "Determine {variable}.",
        "After combining {known} kilograms with an unknown mass {variable}, the scale "
        "reads {total} kilograms. What is {variable}?",
    ],
    "subtraction_remainder": [
        "A tank initially contains {initial} liters. After {removed} liters are removed, "
        "{variable} liters remain. Find {variable}.",
        "Subtracting {removed} from an initial quantity of {initial} leaves {variable}. "
        "Determine {variable}.",
        "A roll was {initial} meters long. Once {removed} meters were used, its remaining "
        "length was {variable} meters. What is {variable}?",
    ],
    "equal_shares": [
        "{total} kilograms are divided equally among {count} boxes. Each box receives "
        "{variable} kilograms. Find {variable}.",
        "When {total} units are shared evenly by {count} recipients, each share is "
        "{variable}. Determine {variable}.",
        "{count} identical containers together hold {total} liters. If each contains "
        "{variable} liters, what is {variable}?",
    ],
    "unit_price": [
        "{count} identical notebooks cost {total} units in total. Their common unit price "
        "is {variable}. Find {variable}.",
        "A purchase of {count} equally priced items totals {total}. The price of one item "
        "is {variable}. Determine {variable}.",
        "The bill for {count} identical tickets is {total}. If one ticket costs {variable}, "
        "what is {variable}?",
    ],
    "rectangle_area": [
        "A rectangle has area {area} square units and width {width} units. Its length is "
        "{variable} units. Find {variable}.",
        "The area of a rectangular panel is {area}. One side measures {width}, while the "
        "adjacent side measures {variable}. Determine {variable}.",
        "A {width}-unit-wide rectangle covers {area} square units. What must its length "
        "{variable} be?",
    ],
    "rectangle_perimeter": [
        "A rectangle has perimeter {perimeter} units and width {width} units. Its length "
        "is {variable} units. Find {variable}.",
        "A rectangular frame has total perimeter {perimeter}. One side is {width}, "
        "and its other side is {variable}. Determine {variable}.",
        "The boundary of a rectangle measures {perimeter} units. If its width is {width} "
        "and its length is {variable}, what is {variable}?",
    ],
    "constant_rate": [
        "An object travels {distance} kilometers in {hours} hours at a constant rate of "
        "{variable} kilometers per hour. Find {variable}.",
        "Covering {distance} kilometers in {hours} hours requires a uniform speed "
        "{variable}. Determine {variable}.",
        "A machine processes {distance} units over {hours} hours without changing pace. "
        "Its hourly rate is {variable}. What is {variable}?",
    ],
    "missing_average": [
        "The arithmetic mean of {known} and {variable} is {mean}. Find {variable}.",
        "Two measurements, {known} and {variable}, have average {mean}. Determine "
        "{variable}.",
        "A pair of scores consists of {known} and {variable}. Their mean is {mean}. What "
        "is the missing score {variable}?",
    ],
    "midpoint": [
        "On a number line, the midpoint of {endpoint} and {variable} is {midpoint}. Find "
        "{variable}.",
        "A segment has endpoints at {endpoint} and {variable}, with midpoint {midpoint}. "
        "Determine {variable}.",
        "The value {midpoint} lies exactly halfway between {endpoint} and {variable}. What "
        "is {variable}?",
    ],
    "map_scale": [
        "On a map, one unit represents {scale} actual units. A distance of {actual} actual "
        "units measures {variable} map units. Find {variable}.",
        "A drawing is reduced by a factor of {scale}. An actual length of {actual} becomes "
        "{variable} in the drawing. Determine {variable}.",
        "Each centimeter in a plan corresponds to {scale} centimeters in reality. A real "
        "segment of {actual} centimeters appears as {variable} centimeters. Find {variable}.",
    ],
    "arithmetic_sequence": [
        "An arithmetic sequence starts at {first}, and term number {index} is {last}. Its "
        "common difference is {variable}. Find {variable}.",
        "Beginning with {first}, an arithmetic progression reaches {last} at position "
        "{index}. Determine its constant step {variable}.",
        "The first term of an arithmetic sequence is {first}; its term at index {index} is "
        "{last}. What is the common difference {variable}?",
    ],
    "equal_edge_path": [
        "A path consists of {edges} edges of equal weight and has total weight {total}. "
        "Each edge has weight {variable}. Find {variable}.",
        "Traversing {edges} equally weighted links produces total cost {total}. The cost of "
        "one link is {variable}. Determine {variable}.",
        "A chain of {edges} identical segments has combined length {total}. If each segment "
        "has length {variable}, what is {variable}?",
    ],
    "percentage": [
        "A quantity {variable} is {percent} percent of {total}. Find {variable}.",
        "Taking {percent} percent of {total} gives {variable}. Determine {variable}.",
        "A portion equal to {percent} percent of a total {total} has value {variable}. What "
        "is {variable}?",
    ],
    "place_value": [
        "Moving the decimal point in the integer {integer} left by {places} positions gives "
        "{variable}. Find {variable}.",
        "Scale the integer {integer} down by {places} decimal places. The result is "
        "{variable}. Determine {variable}.",
        "The decimal {variable} is formed by placing the decimal point {places} digits from "
        "the right in {integer}. What is {variable}?",
    ],
    "quotient": [
        "The quotient of {numerator} divided by {denominator} is {variable}. Find "
        "{variable}.",
        "Dividing {numerator} into {denominator} equal units gives a value {variable} per "
        "unit. Determine {variable}.",
        "The ratio of {numerator} to {denominator} equals {variable}. What is {variable}?",
    ],
}


INTEGRATION_TEMPLATES = [
    "{clues}\n\nUse the recovered value or values to evaluate:\n{expression} = ?",
    "{clues}\n\nAfter determining the unknowns, compute:\n{expression} = ?",
    "Resolve the definition below, then evaluate the resulting decimal expression.\n"
    "{clues}\n\nExpression:\n{expression} = ?",
    "The unknowns in the expression are defined by the following independent problem.\n"
    "{clues}\n\nNow evaluate {expression} = ?",
    "{clues}\n\nSubstitute the recovered value or values into {expression} and calculate its value.",
    "Determine every named quantity from the information below.\n{clues}\n\n"
    "Using those quantities, find the value of {expression}.",
]


TRANSITION_TEMPLATES = [
    "Then define {output_variable} as {intermediate_variable} minus {offset}.",
    "After finding {intermediate_variable}, subtract {offset}; call the result "
    "{output_variable}.",
    "The required value {output_variable} is obtained by decreasing "
    "{intermediate_variable} by {offset}.",
]


FAMILY_GROUPS = {
    "additive": ["additive_balance", "subtraction_remainder"],
    "multiplicative": [
        "equal_shares",
        "unit_price",
        "constant_rate",
        "map_scale",
        "equal_edge_path",
        "percentage",
        "quotient",
    ],
    "geometry": ["rectangle_area", "rectangle_perimeter", "midpoint"],
    "sequence_statistics": ["missing_average", "arithmetic_sequence"],
    "place_value": ["place_value"],
}

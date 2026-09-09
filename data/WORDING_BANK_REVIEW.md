# Decimal subproblem wording-bank review

Automated checks catch placeholder and diversity problems; they do not prove that a wording preserves the intended equation. Review the samples and then inspect the selected bank in full before approving it.

| Bank | Model | Valid families | Valid / unique templates | Integrations | Mean words | Unique bigrams | Built-in copies | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `data/decimal_subproblem_wordings.json` | Qwen3-14B | 9/15 | 106 / 106 | 0 | 11.0 | 63.0% | 6 | approved |

## Side-by-side samples

### additive_balance

**Qwen3-14B**

- No valid candidate.

### subtraction_remainder

**Qwen3-14B**

- A box originally had {initial} items. After {removed} were taken, {variable} remained. What is {variable}?
- {initial} was the starting amount. When {removed} is subtracted, the result is {variable}. Find {variable}.
- If you begin with {initial} and remove {removed}, how much is {variable} left?

### equal_shares

**Qwen3-14B**

- {total} dollars are split evenly among {count} people. Each person receives {variable} dollars. Find {variable}.
- A {total} meter ribbon is divided into {count} equal sections. Each section measures {variable} meters. Determine {variable}.
- {count} workers share {total} hours of overtime. Each worker gets {variable} hours. What is {variable}?

### unit_price

**Qwen3-14B**

- {count} identical items were bought for a total of {total}. The unit price {variable} can be calculated by dividing {total} by {count}. What is {variable}?
- A total of {total} was spent on {count} units of a product. If the unit price is {variable}, solve for {variable}.
- For {count} units priced at {variable} each, the total cost is {total}. What value of {variable} satisfies this equation?

### rectangle_area

**Qwen3-14B**

- No valid candidate.

### rectangle_perimeter

**Qwen3-14B**

- No valid candidate.

### constant_rate

**Qwen3-14B**

- A car drives {distance} miles in {hours} hours. The constant speed is {variable}. Calculate {variable}.
- A factory produces {distance} items in {hours} hours. The rate is {variable}. Find {variable}.
- If {distance} meters are covered in {hours} hours, the constant rate is {variable}. What is {variable}?

### missing_average

**Qwen3-14B**

- The arithmetic mean of {known} and {variable} is {mean}. Find {variable}.
- Two measurements, {known} and {variable}, have average {mean}. Determine {variable}.
- A pair of scores consists of {known} and {variable}. Their mean is {mean}. What is the missing score {variable}?

### midpoint

**Qwen3-14B**

- In a coordinate system, the halfway point between {endpoint} and {variable} is {midpoint}. What is {variable}?
- If {midpoint} is the center of the segment connecting {endpoint} and {variable}, find {variable}.
- The distance from {endpoint} to {midpoint} equals the distance from {midpoint} to {variable}. Determine {variable}.

### map_scale

**Qwen3-14B**

- No valid candidate.

### arithmetic_sequence

**Qwen3-14B**

- An arithmetic sequence begins with {first}, and the term at position {index} equals {last}. What is the common difference {variable}?
- Starting from {first}, the {index}th element of the sequence is {last}. Compute the constant increment {variable}.
- Given the first term {first} and the {index}th term {last}, determine the common difference {variable} of the sequence.

### equal_edge_path

**Qwen3-14B**

- No valid candidate.

### percentage

**Qwen3-14B**

- No valid candidate.

### place_value

**Qwen3-14B**

- Moving the decimal point in the integer {integer} left by {places} positions gives {variable}. Find {variable}.
- Scale the integer {integer} down by {places} decimal places. The result is {variable}. Determine {variable}.
- The decimal {variable} is formed by placing the decimal point {places} digits from the right in {integer}. What is {variable}?

### quotient

**Qwen3-14B**

- When {numerator} is divided by {denominator}, the result is {variable}. Find {variable}.
- Splitting {numerator} into {denominator} equal parts yields {variable} per part. Solve for {variable}.
- The value of {variable} equals {numerator} divided by {denominator}. Calculate {variable}.
